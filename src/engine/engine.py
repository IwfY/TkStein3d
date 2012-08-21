from engine.map import Map
from engine.character import Character
from engine.mathhelper import getPointDistance

from engine.coordinate import Point3D
from datetime import datetime, timedelta
import logging
from operator import itemgetter
from threading import Thread
from time import sleep

class Engine(Thread):
    def __init__(self, canvas):
        Thread.__init__(self)
        self.canvas = canvas
        
        self.map = Map()
        self.player = Character()
        self.viewXRange = 40    # range in which 2D points are displayed
        self.viewYRange = 30
        self.eye = Point3D(0.0, 0.0, -3.0)
        self.millisecondsPerFrame = 500
        logging.basicConfig(filename='/tmp/tkstein3d_engine.log',
                            level=logging.DEBUG, filemode='w')
    
    def run(self):
        while True:
            # time for frame end
            stop = datetime.now() + \
                   timedelta(milliseconds=self.millisecondsPerFrame)
            
            canvasWidth = self.canvas.winfo_width()
            canvasHeight = self.canvas.winfo_height()
            
            polygonsToDraw = []
            
            # generate list of tuples of polygons and distance to eye
            for block in self.map.getBlocks():
                for polygon in block.getPolygons():
                    polygonsToDraw.append(
                            (getPointDistance(self.eye, polygon.getCenter()),
                             polygon))
            
            # sort list
            polygonsToDraw = sorted(polygonsToDraw,
                                    key=itemgetter(0),
                                    reverse=True)
                    
            for polygonToDraw in polygonsToDraw:
                polygon = polygonToDraw[1]
                points = polygon.getPoints2D(
                            self.eye, self.player)
                
                if points is not None:
                    # transform coordinates of view plane to canvas
                    # coordinates  
                    tmpPoints = []
                    for point in points:
                        x = round((point.x + 0.5 * self.viewXRange) * \
                                  canvasWidth / self.viewXRange)
                        y = round((point.y + 0.5 * self.viewYRange) * \
                                  canvasHeight / self.viewYRange)
                        tmpPoints.append(x)
                        tmpPoints.append(y)
                    
                    if polygon.getWidgetId() is None:   # create new widget
                        polygon.setWidgetId(
                                    self.canvas.create_polygon(
                                            tmpPoints[0], tmpPoints[1],
                                            tmpPoints[2], tmpPoints[3],
                                            tmpPoints[4], tmpPoints[5],
                                            tmpPoints[6], tmpPoints[7],
                                            fill='grey', outline='black',
                                            tags='polygon'))
                        logging.debug('newWidget {} {}'.format(
                                        polygon.getWidgetId(), tmpPoints))
                    else:   # move widget
                        logging.debug('movWidget {} {}'.format(
                                        polygon.getWidgetId(), tmpPoints))
                        self.canvas.coords(polygon.getWidgetId(),
                                           tmpPoints[0], tmpPoints[1],
                                           tmpPoints[2], tmpPoints[3],
                                           tmpPoints[4], tmpPoints[5],
                                           tmpPoints[6], tmpPoints[7])
            
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
