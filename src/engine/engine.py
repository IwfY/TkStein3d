from engine.map import Map
from engine.character import Character

from engine.coordinate import Point3D
from datetime import datetime, timedelta
from threading import Thread
from time import sleep

class Engine(Thread):
    def __init__(self, canvas):
        Thread.__init__(self)
        self.map = Map()
        self.player = Character()
        self.canvas = canvas
        self.viewXRange = 40    # range in which 2D points are displayed
        self.viewYRange = 30
        self.eye = Point3D(0.0, 0.0, -3.0)
        self.millisecondsPerFrame = 15
    
    def run(self):
        while True:
            # time for frame end
            stop = datetime.now() + \
                   timedelta(milliseconds=self.millisecondsPerFrame)
            
            canvasWidth = self.canvas.winfo_width()
            canvasHeight = self.canvas.winfo_height()
            
            self.canvas.delete('polygon')
            for block in self.map.getBlocks():
                for polygon in block.getPolygons():
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
                        self.canvas.create_polygon(tmpPoints,
                                                   fill='grey', outline='black',
                                                   tags='polygon')
            
            # time till frame end
            remaining = stop - datetime.now()
            if remaining.days < 0:  # needed more then 15 milliseconds
                print('remaining:',
                      round(-1000 + remaining.microseconds / 1000, 1),
                      '/', self.millisecondsPerFrame)
                remaining = -1
            else:
                remaining = round(remaining.microseconds / 1000000, 3)
                print('remaining: ', remaining * 1000, '/', 
                      self.millisecondsPerFrame)
            if remaining > 0:
                sleep(remaining)
