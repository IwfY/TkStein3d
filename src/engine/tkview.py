from engine.coordinate import Point3D, Vector3D
from engine.infoclass import InfoClass
from engine.mathhelper import getPointDistance, getIntersectionXYPlane,\
    getSquaredPointDistance
from engine.polygon import moveAndRotatePolygon, Polygon


from datetime import datetime, timedelta
import logging
from operator import attrgetter
from threading import Thread
from time import sleep
from tkinter.constants import ALL, HIDDEN, NORMAL 
from tkinter.ttk import _flatten
import cProfile


class TkView(Thread):
    def __init__(self, client, canvas):
        Thread.__init__(self)
        
        self.client = client
        self.canvas = canvas
        
        self.gameMap = client.getGameMap()
        
        self.viewXRange = 4    # range in which 2D points are displayed
        self.viewYRange = 3
        self.eye = Point3D(0.0, 0.0, -2.0)
        self.millisecondsPerFrame = 50
        self.running = False
        
        self.lastPolygonId = 0
        
        logging.basicConfig(filename='tkstein3d_engine.log',
                            level=logging.DEBUG, filemode='w')
    
    def getNewPolygonTag(self):
        newPolygonId = 'p{}'.format(self.lastPolygonId)
        self.lastPolygonId += 1
            
        return newPolygonId
    
    
    def stop(self):
        '''stop the loop from running'''
        self.running = False
    
    def run(self):
        '''rename this to run and run to _run for profiling output'''
        profiler = cProfile.Profile()
        try:
            return profiler.runcall(self._run)
        finally:
            profiler.print_stats()
    
    def _run(self):
        
        orderedPolygonTagsLastFrame = []
        
        activeBuffer = 0
        
        #draw ground/ ceiling
        canvasWidth = 1
        canvasHeight = 1
        #sometimes canvas dimensions can't be loaded first time
        while canvasWidth == 1 or canvasHeight == 1:
            canvasWidth = self.canvas.winfo_width()
            canvasHeight = self.canvas.winfo_height()
        
        # sky
        self.canvas.create_rectangle(0, 0, canvasWidth, canvasHeight / 2,
                                     fill=self.gameMap.getSkyColor())
        # floor
        self.canvas.create_rectangle(0, canvasHeight / 2,
                                     canvasWidth, canvasHeight,
                                     fill=self.gameMap.getGroundColor())
        
        self.running = True
        while self.running:
            # time for frame end
            stop = datetime.now() + \
                   timedelta(milliseconds=self.millisecondsPerFrame)
            stopWatchTime = datetime.now()
            
            
            ##########################################
            # DRAWING
            ##########################################
            
            canvasWidth = self.canvas.winfo_width()
            canvasHeight = self.canvas.winfo_height()
            
            # generate list of tuples of polygons and distance to eye
            ##########################################
            player = self.client.getPlayer()
            playerPostion = player.getPosition()
            moveVector = Vector3D(-playerPostion.x,
                                -playerPostion.y,
                                -playerPostion.z)
            polygonsToDraw = []
            for polygonOriginal in self.gameMap.getPolygons():
                polygon = moveAndRotatePolygon(polygonOriginal,
                                               moveVector,
                                               self.eye,
                                               player.getViewAngle())
                info = InfoClass()
                info.polygon = polygon
                info.polygonOriginal = polygonOriginal
                # using squared distance as it's for comparison only 
                info.distanceToEye = getSquaredPointDistance(
                                          self.eye,
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
            
            
            # check for normals corresponding to view vector
            ##########################################
            for polygonToDraw in polygonsToDraw:
                if polygonToDraw.state == NORMAL:
                    if not polygonToDraw.polygon.polygonFacesPoint(self.eye):
                        polygonToDraw.state = HIDDEN
            logging.debug('normal-view angle check: {} msec'.format(
                        (datetime.now() - stopWatchTime).microseconds / 1000))
            stopWatchTime = datetime.now()
            
            # exchange polygon tags to match drawing order
            ##########################################
            
            # get number of polygons to be drawn
            stateNormalCount = 0
            for i in range(len(polygonsToDraw)):
                if polygonsToDraw[i].state == NORMAL:
                    stateNormalCount += 1
            logging.debug('polycount {}'.format(stateNormalCount))    
            
            # create additional polygons
            for i in range(stateNormalCount - len(orderedPolygonTagsLastFrame)):
                id0 = self.canvas.create_polygon(
                        (0.0, 0.0, 0.0, 0.0),
                        state=HIDDEN)
                id1 = self.canvas.create_polygon(
                        (0.0, 0.0, 0.0, 0.0),
                        state=HIDDEN)
                # save tag order
                orderedPolygonTagsLastFrame.append((id0, id1))
            
            # set hide state for surplus polygons
            surplusCount = len(orderedPolygonTagsLastFrame) - stateNormalCount
            
            # set tags
            indexOrderedPolygons = 0
            for i in range(len(polygonsToDraw)):
                if polygonsToDraw[i].state == NORMAL:
                    polygonsToDraw[i].polygonOriginal.\
                            setPolygonId(orderedPolygonTagsLastFrame[
                                            indexOrderedPolygons][activeBuffer])
                    indexOrderedPolygons += 1
                else:
                    polygonsToDraw[i].polygonOriginal.setPolygonId(None)
            
            logging.debug('polygon creation, assignment: {} msec'.format(
                        (datetime.now() - stopWatchTime).microseconds / 1000))
            stopWatchTime = datetime.now()
            
            
            # transform coordinates of view plane to canvas coordinates
            ##########################################
            polygon2DPointsList = []    
            for polygonToDraw in polygonsToDraw:
                if polygonToDraw.state == NORMAL:
                    polygon = polygonToDraw.polygon
                    points = polygon.getPoints2D(
                                self.eye, player)
                    if points is not None:                    
                        tmpPoints = InfoClass()
                        tmpPoints.polygonOriginal = polygonToDraw. \
                                                        polygonOriginal
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
            stateNormalWidgets = []
            
            i = 0
            for polygon2DPoints in polygon2DPointsList:
                polygonOriginal = polygon2DPoints.polygonOriginal
                points = polygon2DPoints.points
                
                polygonWidgetId = polygonOriginal.getPolygonId()                
                
                if polygonWidgetId is not None:
                    # get active polygon id
                    if polygon2DPoints.state == NORMAL:
                        i += 1
                        self.canvas.itemconfig(polygonWidgetId,
                                               fill=polygonOriginal.fill,
                                               outline=polygonOriginal.outline)
                        self.canvas.coords(polygonWidgetId,
                                           _flatten(points))
                        stateNormalWidgets.append(polygonWidgetId)
            logging.debug('draw update: {} msec'.format(
                        (datetime.now() - stopWatchTime).microseconds / 1000))
            logging.debug('polygons moved: {}'.format(i))
            stopWatchTime = datetime.now()
            
            # switch display buffers
            ##########################################
            inactiveBuffer = int(not activeBuffer)
            
            for polygonTuple in orderedPolygonTagsLastFrame:
                if polygonTuple[activeBuffer] in stateNormalWidgets:
                    self.canvas.itemconfig(polygonTuple[activeBuffer],
                                           state=NORMAL)
            for polygonTuple in orderedPolygonTagsLastFrame:
                if polygonTuple[activeBuffer] not in stateNormalWidgets:
                    self.canvas.itemconfig(polygonTuple[activeBuffer],
                                           state=HIDDEN)
            for polygonTuple in orderedPolygonTagsLastFrame:
                self.canvas.itemconfig(polygonTuple[inactiveBuffer],
                                       state=HIDDEN)
            
            
            # remove surplus polygons
            surplusCount = len(orderedPolygonTagsLastFrame) - stateNormalCount
            for i in range(surplusCount):
                self.canvas.delete(orderedPolygonTagsLastFrame[-1])
                orderedPolygonTagsLastFrame = orderedPolygonTagsLastFrame[:-1]
            
            activeBuffer = int(not activeBuffer)
            
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

