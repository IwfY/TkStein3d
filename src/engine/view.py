from engine.mathhelper import getPointDistance
from engine.polygon import moveAndRotatePolygon

from engine.coordinate import Point3D

from datetime import datetime, timedelta
import logging
from operator import attrgetter
from threading import Thread
from time import sleep
from engine.infoclass import InfoClass

class View(Thread):
    def __init__(self, gameManager, gameMap, character, canvas):
        Thread.__init__(self)
        self.canvas = canvas
        self.gameManager = gameManager
        
        self.gameMap = gameMap
        self.player = character
        self.viewXRange = 4    # range in which 2D points are displayed
        self.viewYRange = 3
        self.eye = Point3D(0.0, 0.0, -1.0)
        self.millisecondsPerFrame = 100
        logging.basicConfig(filename='/tmp/tkstein3d_engine.log',
                            level=logging.DEBUG, filemode='w')
    
    def run(self):
        while True:
            # time for frame end
            stop = datetime.now() + \
                   timedelta(milliseconds=self.millisecondsPerFrame)
            
            canvasWidth = self.canvas.winfo_width()
            canvasHeight = self.canvas.winfo_height()
            
            # generate list of tuples of polygons and distance to eye
            polygonsToDraw = []
            for block in self.gameMap.getBlocks():
                for polygon in block.getPolygons():
                    polygon = moveAndRotatePolygon(polygon,
                                                   self.player.getPosition(),
                                                   0.0)
                    info = InfoClass()
                    info.polygon = polygon
                    info.distanceToEye = getPointDistance(self.eye,
                                                          polygon.getCenter())
                    polygonsToDraw.append(info)
            
            # sort list
            polygonsToDraw = sorted(polygonsToDraw,
                                    key=attrgetter('distanceToEye'),
                                    reverse=True)
            
            # transform coordinates of view plane to canvas coordinates
            polygon2DPointsList = []    
            for polygonToDraw in polygonsToDraw:
                polygon = polygonToDraw.polygon
                points = polygon.getPoints2D(
                            self.eye, self.player)
                if points is not None:                    
                    tmpPoints = InfoClass()
                    tmpPoints.polygon = polygon
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
            for polygon2DPoints in polygon2DPointsList:
                polygon = polygon2DPoints.polygon
                points = polygon2DPoints.points
                
                if polygon.getWidgetId() is None:   # create new widget
                    polygon.setWidgetId(
                                self.canvas.create_polygon(
                                        points[0], points[1],
                                        points[2], points[3],
                                        points[4], points[5],
                                        points[6], points[7],
                                        fill='grey', outline='black',
                                        tags='polygon'))
                    logging.debug('newWidget {} {}'.format(
                                    polygon.getWidgetId(), points))
                else:   # move widget
                    logging.debug('movWidget {} {}'.format(
                                    polygon.getWidgetId(), points))
                    self.canvas.coords(polygon.getWidgetId(),
                                       points[0], points[1],
                                       points[2], points[3],
                                       points[4], points[5],
                                       points[6], points[7])
            
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

    def getCanvas(self):
        return self.canvas