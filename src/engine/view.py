from engine.coordinate import Point3D, Vector3D
from engine.infoclass import InfoClass
from engine.mathhelper import getIntersectionXYPlane, getPointDistance
from engine.polygon import moveAndRotatePolygon, Polygon

from datetime import datetime, timedelta
import logging
from operator import attrgetter
from threading import Thread, Lock
from time import sleep
from tkinter import _flatten, ALL, HIDDEN, NORMAL


class View(Thread):
    count = 0
    mutex = Lock()
    
    def __init__(self, gameManager, gameMap, character, window, canvas):
        Thread.__init__(self)
        self.canvas = canvas
        self.window = window
        self.gameManager = gameManager
        self.keysPressed = set()
        
        self.gameMap = gameMap
        self.player = character
        self.viewXRange = 4    # range in which 2D points are displayed
        self.viewYRange = 3
        self.eye = Point3D(0.0, 0.0, -2.0)
        self.millisecondsPerFrame = 60
        #logging.basicConfig(filename='/tmp/tkstein3d_engine.log',
        #                    level=logging.CRITICAL, filemode='w')
        logging.basicConfig(filename='/tmp/tkstein3d_engine.log',
                            level=logging.DEBUG, filemode='w')


    def getNewPolygonTag(self):
        # using mutex for unique IDs if several threads create polygon tags
        View.mutex.acquire()
        try:
            newPolygonId = 'p{}'.format(View.count)
            View.count += 1
        finally:
            View.mutex.release()
            
        return newPolygonId


    def run(self):
        self.setBindings()
        
        orderedPolygonTagsLastFrame = []
        
        activeBuffer = 'buffer1'
        inactiveBuffer = 'buffer2'
        
        #draw ground/ ceiling
        canvasWidth = 1
        canvasHeight = 1
        #sometimes canvas dimensions can't be loaded first time
        while canvasWidth ==1 or canvasHeight == 1:
            canvasWidth = self.canvas.winfo_width()
            canvasHeight = self.canvas.winfo_height()
        self.canvas.create_rectangle(0, 0, canvasWidth, canvasHeight / 2,
                                     fill=self.gameMap.getSkyColor())
        self.canvas.create_rectangle(0, canvasHeight / 2,
                                     canvasWidth, canvasHeight,
                                     fill=self.gameMap.getGroundColor())
        
        while True:
            # time for frame end
            stop = datetime.now() + \
                   timedelta(milliseconds=self.millisecondsPerFrame)
            stopWatchTime = datetime.now()
            
            ##########################################
            # INPUT
            ##########################################
            moveDeltaForward = 0.0
            moveDeltaLeft = 0.0
            rotation = 0.0
            # copy set because of error when set size changes during iteration
            tmpKeysPressed = set(self.keysPressed)
            for key in tmpKeysPressed:
                if key == 65363:    # right array
                    rotation += 0.075
                elif key == 65361:  # left array
                    rotation -= 0.075
                if key == 119:      # w
                    moveDeltaForward += 1.0
                elif key == 115:    # s
                    moveDeltaForward -= 1.0
                elif key == 97:     # a
                    moveDeltaLeft -= 1.0
                elif key == 100:    # d
                    moveDeltaLeft += 1.0
            self.gameManager.moveRotateCharacter(self.player,
                                                 moveDeltaForward,
                                                 moveDeltaLeft,
                                                 rotation)
            logging.debug('input: in {} msec'.format(
                        (datetime.now() - stopWatchTime).microseconds / 1000))
            stopWatchTime = datetime.now()
            
            
            ##########################################
            # DRAWING
            ##########################################
            
            canvasWidth = self.canvas.winfo_width()
            canvasHeight = self.canvas.winfo_height()
            
            # generate list of tuples of polygons and distance to eye
            ##########################################
            playerPostion = self.player.getPosition()
            moveVector = Vector3D(-playerPostion.x,
                                -playerPostion.y,
                                -playerPostion.z)
            polygonsToDraw = []
            for polygonOriginal in self.gameMap.getPolygons():
                polygon = moveAndRotatePolygon(polygonOriginal,
                                               moveVector,
                                               self.eye,
                                               self.player.getViewAngle())
                info = InfoClass()
                info.polygon = polygon
                info.polygonOriginal = polygonOriginal
                info.distanceToEye = getPointDistance(self.eye,
                                                      polygon.getCenter())
                polygonsToDraw.append(info)
            logging.debug('move and rotate polygons: {} msec'.format(
                        (datetime.now() - stopWatchTime).microseconds / 1000))
            stopWatchTime = datetime.now()
            
            # sort list
            ##########################################
            polygonsToDraw = sorted(polygonsToDraw,
                                    key=attrgetter('distanceToEye'),
                                    reverse=True)
            logging.debug('sorting list: {} msec'.format(
                        (datetime.now() - stopWatchTime).microseconds / 1000))
            stopWatchTime = datetime.now()
            
            
            # check for position towards x-y-plane
            ##########################################
            for polygonToDraw in polygonsToDraw:
                polygon = polygonToDraw.polygon
                polygonOriginal = polygonToDraw.polygonOriginal
                polygonToDraw.state = NORMAL
                
                newPoints = []
                oldPoints = polygon.getPoints3D()
                for i in range(len(oldPoints)):
                    cursor = oldPoints[i]
                    cursorSuccessor = oldPoints[0]
                    if i != len(oldPoints) - 1:
                        cursorSuccessor = oldPoints[i + 1]
                     
                    if cursorSuccessor.z >= 0.0:
                        if cursor.z < 0.0:
                            tmpPointCoordinates = \
                                getIntersectionXYPlane(cursor,
                                                       cursorSuccessor)
                            tmpPoint = Point3D(tmpPointCoordinates[0],
                                               tmpPointCoordinates[1],
                                               0.0)
                            newPoints.append(tmpPoint)
                        newPoints.append(cursorSuccessor)
                    elif cursor.z > 0:  # and cursorSuccessor.z < 0.0
                        tmpPointCoordinates = \
                                getIntersectionXYPlane(cursor,
                                                       cursorSuccessor)
                        tmpPoint = Point3D(tmpPointCoordinates[0],
                                           tmpPointCoordinates[1],
                                           0.0)
                        newPoints.append(tmpPoint)
                
                if len(newPoints) == 0:
                    polygonToDraw.state = HIDDEN
                else:
                    polygonToDraw.polygon = \
                            Polygon(polygonOriginal.getPolygonId(), newPoints)
            logging.debug('xy-plane intersection: {} msec'.format(
                        (datetime.now() - stopWatchTime).microseconds / 1000))
            stopWatchTime = datetime.now()
                            
            
            
            # exchange polygon tags to match drawing order
            ##########################################
            
            # get number of polygons to be drawn
            stateNormalCount = 0
            for i in range(len(polygonsToDraw)):
                if polygonsToDraw[i].state == NORMAL:
                    stateNormalCount += 1
            
            # create additional polygons
            for i in range(stateNormalCount - len(orderedPolygonTagsLastFrame)):
                newPolygonTag = self.getNewPolygonTag()
                self.canvas.create_polygon(
                        (0.0, 0.0, 0.0, 0.0),
                        state=HIDDEN,
                        tags=(newPolygonTag, activeBuffer))
                self.canvas.create_polygon(
                        (0.0, 0.0, 0.0, 0.0),
                        state=HIDDEN,
                        tags=(newPolygonTag, inactiveBuffer))
                # save tag order
                orderedPolygonTagsLastFrame.append(newPolygonTag)
            
            # set hide state for surplus polygons
            surplusCount = len(orderedPolygonTagsLastFrame) - stateNormalCount
            for i in range(surplusCount):
                self.canvas.addtag_withtag('hide', orderedPolygonTagsLastFrame[-1 - i])
            
            # set tags
            indexOrderedPolygons = 0
            for i in range(len(polygonsToDraw)):
                if polygonsToDraw[i].state == NORMAL:
                    polygonsToDraw[i].polygonOriginal.\
                            setPolygonId(orderedPolygonTagsLastFrame[
                                            indexOrderedPolygons])
                    indexOrderedPolygons += 1
                else:
                    polygonsToDraw[i].polygonOriginal.setPolygonId('None')
            
            logging.debug('polygon creation, assignment: {} msec'.format(
                        (datetime.now() - stopWatchTime).microseconds / 1000))
            stopWatchTime = datetime.now()
            
            
            # transform coordinates of view plane to canvas coordinates
            ##########################################
            polygon2DPointsList = []    
            for polygonToDraw in polygonsToDraw:
                polygon = polygonToDraw.polygon
                points = polygon.getPoints2D(
                            self.eye, self.player)
                if points is not None:                    
                    tmpPoints = InfoClass()
                    tmpPoints.polygonOriginal = polygonToDraw.polygonOriginal
                    tmpPoints.state = polygonToDraw.state
                    tmpPoints.points = []
                    for point in points:
                        x = round((point.x + 0.5 * self.viewXRange) * \
                                  canvasWidth / self.viewXRange)
                        y = round((-point.y + 0.5 * self.viewYRange) * \
                                  canvasHeight / self.viewYRange)
                        tmpPoints.points.append(x)
                        tmpPoints.points.append(y)
                    
                    polygon2DPointsList.append(tmpPoints)
            logging.debug('3d-2d conversion: {} msec'.format(
                        (datetime.now() - stopWatchTime).microseconds / 1000))
            stopWatchTime = datetime.now()
            
            
            # draw
            ##########################################
            
            # remove show/hide tags
            self.canvas.dtag(ALL, 'normal')
            self.canvas.dtag(ALL, 'hide')
            
            i = 0
            for polygon2DPoints in polygon2DPointsList:
                polygonOriginal = polygon2DPoints.polygonOriginal
                points = polygon2DPoints.points
                
                polygonWidgetIds = self.canvas.find_withtag(
                                        polygonOriginal.getPolygonId())
                activeWidgetIds = self.canvas.find_withtag(activeBuffer)
                
                polygonWidgetId = [r for r in polygonWidgetIds \
                                   if r in activeWidgetIds]
                
                
                if len(polygonWidgetId) >= 1:
                    polygonWidgetId = polygonWidgetId[0]
                    # get active polygon id
                    if polygon2DPoints.state == NORMAL:
                        i += 1
                        self.canvas.itemconfig(polygonWidgetId,
                                               fill=polygonOriginal.fill,
                                               outline=polygonOriginal.outline)
                        self.canvas.coords(polygonWidgetId,
                                           _flatten(points))
                        self.canvas.addtag_withtag('normal', polygonWidgetId)
                    else:
                        self.canvas.addtag_withtag('hide', polygonWidgetId)
            logging.debug('draw update: {} msec'.format(
                        (datetime.now() - stopWatchTime).microseconds / 1000))
            logging.debug('polygons moved: {}'.format(i))
            stopWatchTime = datetime.now()
            
            # switch display buffers
            ##########################################
            self.canvas.itemconfig('normal',
                                   state=NORMAL)
            self.canvas.itemconfig('hide',
                                   state=HIDDEN)
            self.canvas.itemconfig(inactiveBuffer,
                                   state=HIDDEN)
            
            # remove surplus polygons
            surplusCount = len(orderedPolygonTagsLastFrame) - stateNormalCount
            for i in range(surplusCount):
                self.canvas.delete(orderedPolygonTagsLastFrame[-1])
                orderedPolygonTagsLastFrame = orderedPolygonTagsLastFrame[:-1]
            
            tmp = activeBuffer
            activeBuffer = inactiveBuffer
            inactiveBuffer = tmp
            
            logging.debug('buffer switching: {} msec'.format(
                        (datetime.now() - stopWatchTime).microseconds / 1000))
            
            # time till frame end
            remaining = stop - datetime.now()
            if remaining.days < 0:  # frame needed too long
                logging.debug('  remaining: {}/{} msec'.format(
                      round(-1000 + remaining.microseconds / 1000, 1),
                      self.millisecondsPerFrame))
                remaining = -1
            else:
                remaining = round(remaining.microseconds / 1000000, 3)
                logging.debug('  remaining: {}/{} msec'.format(remaining * 1000, 
                      self.millisecondsPerFrame))
            if remaining > 0:
                sleep(remaining)


    def setBindings(self):
        self.window.bind('<KeyPress>', self.keyPressed)
        self.window.bind('<KeyRelease>', self.keyReleased)


    def keyPressed(self, event):
        self.keysPressed.add(event.keysym_num)


    def keyReleased(self, event):
        if event.keysym_num in self.keysPressed:
            self.keysPressed.remove(event.keysym_num)


    def getCanvas(self):
        return self.canvas