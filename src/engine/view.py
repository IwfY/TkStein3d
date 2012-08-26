from engine.coordinate import Point3D, Vector3D
from engine.infoclass import InfoClass
from engine.mathhelper import getPointDistance
from engine.polygon import moveAndRotatePolygon

from datetime import datetime, timedelta
import logging
from operator import attrgetter
from threading import Thread
from time import sleep
from tkinter import _flatten, HIDDEN, NORMAL


class View(Thread):
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
        logging.basicConfig(filename='/tmp/tkstein3d_engine.log',
                            level=logging.DEBUG, filemode='w')
    
    def run(self):
        self.setBindings()
        
        orderedPolygonTagsLastFrame = []
        
        while True:
            # time for frame end
            stop = datetime.now() + \
                   timedelta(milliseconds=self.millisecondsPerFrame)
            
            #INPUT
            ######################
            moveDeltaForward = 0.0
            moveDeltaLeft = 0.0
            rotation = 0.0
            # copy set because of error when set size changes during iteration
            tmpKeysPressed = set(self.keysPressed)
            for key in tmpKeysPressed:
                if key == 65363:    # right array
                    rotation += 0.05
                elif key == 65361:  # left array
                    rotation -= 0.05
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
            
            #DRAWING
            ######################
            
            canvasWidth = self.canvas.winfo_width()
            canvasHeight = self.canvas.winfo_height()
            
            # generate list of tuples of polygons and distance to eye
            polygonsToDraw = []
            for mapObject in self.gameMap.getObjects():
                for polygonOriginal in mapObject.getPolygons():
                    polygon = moveAndRotatePolygon(polygonOriginal,
                                                   self.player.getPosition(),
                                                   self.eye,
                                                   self.player.getViewAngle())
                    info = InfoClass()
                    info.polygon = polygon
                    info.polygonOriginal = polygonOriginal
                    info.distanceToEye = getPointDistance(self.eye,
                                                          polygon.getCenter())
                    polygonsToDraw.append(info)
            
            # sort list
            polygonsToDraw = sorted(polygonsToDraw,
                                    key=attrgetter('distanceToEye'),
                                    reverse=True)
            
            # check for position towards x-y-plane
            for polygonToDraw in polygonsToDraw:
                polygon = polygonToDraw.polygon
                polygonToDraw.state = NORMAL
                for point in polygon.getPoints3D():
                    if point.z < 0.0:
                        polygonToDraw.state = HIDDEN
            
            # exchange polygon tags to match drawing order
            if len(orderedPolygonTagsLastFrame) != 0:
                for i in range(0, len(polygonsToDraw)):
                    polygonsToDraw[i].polygonOriginal.setPolygonId(
                            orderedPolygonTagsLastFrame[i])
            
            # transform coordinates of view plane to canvas coordinates
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
                        y = round((point.y + 0.5 * self.viewYRange) * \
                                  canvasHeight / self.viewYRange)
                        tmpPoints.points.append(x)
                        tmpPoints.points.append(y)
                    
                    polygon2DPointsList.append(tmpPoints)
            
            # draw
            i = 0
            for polygon2DPoints in polygon2DPointsList:
                polygonOriginal = polygon2DPoints.polygonOriginal
                points = polygon2DPoints.points
                
                polygonWidgetId = self.canvas.find_withtag(
                                        polygonOriginal.getPolygonId())
                if len(polygonWidgetId) == 0:   # create new widget
                    self.canvas.create_polygon(
                            _flatten(points),
                            fill='grey', outline='black',
                            state=polygon2DPoints.state,
                            tags=polygonOriginal.getPolygonId())
                    # save tag order
                    orderedPolygonTagsLastFrame.append(
                            polygonOriginal.getPolygonId())
                    logging.debug('newWidget {} {}'.format(
                                    polygonOriginal.getPolygonId(), points))
                else:   # move widget
                    self.canvas.itemconfig(polygonWidgetId,
                                           state=polygon2DPoints.state)
                    if polygon2DPoints.state == NORMAL:
                        self.canvas.coords(polygonWidgetId,
                                           _flatten(points))
                        logging.debug('movWidget {} {}'.format(
                                        polygonOriginal.getPolygonId(), points))
                        
            
            # time till frame end
            remaining = stop - datetime.now()
            if remaining.days < 0:  # frame needed too long
                logging.debug('remaining: {}/{} msec'.format(
                      round(-1000 + remaining.microseconds / 1000, 1),
                      self.millisecondsPerFrame))
                remaining = -1
            else:
                remaining = round(remaining.microseconds / 1000000, 3)
                logging.debug('remaining: {}/{} msec'.format(remaining * 1000, 
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