'''
Created on Jan 21, 2013

@author: marcel
'''
import unittest
from engine.server.gridmap import GridMap
from engine.shared.coordinate import Point3D


class GridMapTest(unittest.TestCase):


    def testFloorAndCeiling(self):
        grid = [[1]]
        
        gridMap = GridMap(None, grid, 1.0)
        
        polygons = gridMap.getStaticPolygons()
        self.assertEqual(len(polygons), 2)
        
        targetPointsList = [
                            [(0.0, -0.5, 0.0),    # floor
                             (0.0, -0.5, 1.0),
                             (1.0, -0.5, 1.0),
                             (1.0, -0.5, 0.0)],
                            
                            [(0.0, 0.5, 0.0),    # ceiling
                             (1.0, 0.5, 0.0),
                             (1.0, 0.5, 1.0),
                             (0.0, 0.5, 1.0)]
                            ]
        
        for polygon in polygons:
            points = polygon.getPoints3D()
            self.assertEqual(len(points), 4)
            pointTuples = [(points[0].x, points[0].y, points[0].z),
                            (points[1].x, points[1].y, points[1].z),
                            (points[2].x, points[2].y, points[2].z),
                            (points[3].x, points[3].y, points[3].z)]
            
            
            targetPointsFound = False
            for targetPoints in targetPointsList:
                if pointTuples[0] in targetPoints and \
                        pointTuples[1] in targetPoints and \
                        pointTuples[2] in targetPoints and \
                        pointTuples[3] in targetPoints:    # all points equal
                    
                    #check order
                    index = targetPoints.index(pointTuples[0])
                    self.assertEqual(targetPoints.index(pointTuples[1]),
                                     (index + 1) % 4, 'points in wrong order')
                    targetPointsFound = True
                    break
            
            self.assertTrue(targetPointsFound,
                            'No corresponding points group found for polygon')
    
    def testWall12(self):
        grid = [[1, 2]]
        
        gridMap = GridMap(None, grid, 1.0)
        
        polygons = gridMap.getStaticPolygons()
        self.assertEqual(len(polygons), 3)
        
        targetPointsList = [
                            [(0.0, -0.5, 0.0),    # floor
                             (0.0, -0.5, 1.0),
                             (1.0, -0.5, 1.0),
                             (1.0, -0.5, 0.0)],
                            
                            [(0.0, 0.5, 0.0),    # ceiling
                             (1.0, 0.5, 0.0),
                             (1.0, 0.5, 1.0),
                             (0.0, 0.5, 1.0)],
                            
                            [(1.0, -0.5, 0.0),    # wall
                             (1.0, -0.5, 1.0),
                             (1.0,  0.5, 1.0),
                             (1.0,  0.5, 0.0)]
                            ]
        
        for polygon in polygons:
            points = polygon.getPoints3D()
            self.assertEqual(len(points), 4)
            pointTuples = [(points[0].x, points[0].y, points[0].z),
                            (points[1].x, points[1].y, points[1].z),
                            (points[2].x, points[2].y, points[2].z),
                            (points[3].x, points[3].y, points[3].z)]
            
            targetPointsFound = False
            for targetPoints in targetPointsList:
                if pointTuples[0] in targetPoints and \
                        pointTuples[1] in targetPoints and \
                        pointTuples[2] in targetPoints and \
                        pointTuples[3] in targetPoints:    # all points equal
                    
                    #check order
                    index = targetPoints.index(pointTuples[0])
                    self.assertEqual(targetPoints.index(pointTuples[1]),
                                     (index + 1) % 4, 'points in wrong order')
                    targetPointsFound = True
                    break
            
            self.assertTrue(targetPointsFound,
                            'No corresponding points group found for polygon')
    
    def testWall21(self):
        grid = [[2, 1]]
        
        gridMap = GridMap(None, grid, 1.0)
        
        polygons = gridMap.getStaticPolygons()
        self.assertEqual(len(polygons), 3)
        
        targetPointsList = [
                            [(1.0, -0.5, 0.0),    # floor
                             (1.0, -0.5, 1.0),
                             (2.0, -0.5, 1.0),
                             (2.0, -0.5, 0.0)],
                            
                            [(1.0, 0.5, 0.0),    # ceiling
                             (2.0, 0.5, 0.0),
                             (2.0, 0.5, 1.0),
                             (1.0, 0.5, 1.0)],
                            
                            [(1.0, -0.5, 1.0),    # wall
                             (1.0, -0.5, 0.0),
                             (1.0,  0.5, 0.0),
                             (1.0,  0.5, 1.0)]
                            ]
        
        for polygon in polygons:
            points = polygon.getPoints3D()
            self.assertEqual(len(points), 4)
            pointTuples = [(points[0].x, points[0].y, points[0].z),
                            (points[1].x, points[1].y, points[1].z),
                            (points[2].x, points[2].y, points[2].z),
                            (points[3].x, points[3].y, points[3].z)]
            
            targetPointsFound = False
            for targetPoints in targetPointsList:
                if pointTuples[0] in targetPoints and \
                        pointTuples[1] in targetPoints and \
                        pointTuples[2] in targetPoints and \
                        pointTuples[3] in targetPoints:    # all points equal
                    
                    #check order
                    index = targetPoints.index(pointTuples[0])
                    self.assertEqual(targetPoints.index(pointTuples[1]),
                                     (index + 1) % 4, 'points in wrong order')
                    targetPointsFound = True
                    break
            
            self.assertTrue(targetPointsFound,
                            'No corresponding points group found for polygon')
    
    def testWall1over2(self):
        grid = [[1], [2]]
        
        gridMap = GridMap(None, grid, 1.0)
        
        polygons = gridMap.getStaticPolygons()
        self.assertEqual(len(polygons), 3)
        
        targetPointsList = [
                            [(0.0, -0.5, 0.0),    # floor
                             (0.0, -0.5, 1.0),
                             (1.0, -0.5, 1.0),
                             (1.0, -0.5, 0.0)],
                            
                            [(0.0, 0.5, 0.0),    # ceiling
                             (1.0, 0.5, 0.0),
                             (1.0, 0.5, 1.0),
                             (0.0, 0.5, 1.0)],
                            
                            [(1.0, -0.5, 1.0),    # wall
                             (0.0, -0.5, 1.0),
                             (0.0,  0.5, 1.0),
                             (1.0,  0.5, 1.0)]
                            ]
        
        for polygon in polygons:
            points = polygon.getPoints3D()
            self.assertEqual(len(points), 4)
            pointTuples = [(points[0].x, points[0].y, points[0].z),
                            (points[1].x, points[1].y, points[1].z),
                            (points[2].x, points[2].y, points[2].z),
                            (points[3].x, points[3].y, points[3].z)]
            
            targetPointsFound = False
            for targetPoints in targetPointsList:
                if pointTuples[0] in targetPoints and \
                        pointTuples[1] in targetPoints and \
                        pointTuples[2] in targetPoints and \
                        pointTuples[3] in targetPoints:    # all points equal
                    
                    #check order
                    index = targetPoints.index(pointTuples[0])
                    self.assertEqual(targetPoints.index(pointTuples[1]),
                                     (index + 1) % 4, 'points in wrong order')
                    targetPointsFound = True
                    break
            
            self.assertTrue(targetPointsFound,
                            'No corresponding points group found for polygon')
    
    
    def testWall2over1(self):
        grid = [[2], [1]]
        
        gridMap = GridMap(None, grid, 1.0)
        
        polygons = gridMap.getStaticPolygons()
        self.assertEqual(len(polygons), 3)
        
        targetPointsList = [
                            [(0.0, -0.5, 1.0),    # floor
                             (0.0, -0.5, 2.0),
                             (1.0, -0.5, 2.0),
                             (1.0, -0.5, 1.0)],
                            
                            [(0.0, 0.5, 1.0),    # ceiling
                             (1.0, 0.5, 1.0),
                             (1.0, 0.5, 2.0),
                             (0.0, 0.5, 2.0)],
                            
                            [(0.0, -0.5, 1.0),    # wall
                             (1.0, -0.5, 1.0),
                             (1.0,  0.5, 1.0),
                             (0.0,  0.5, 1.0)]
                            ]
        
        for polygon in polygons:
            points = polygon.getPoints3D()
            self.assertEqual(len(points), 4)
            pointTuples = [(points[0].x, points[0].y, points[0].z),
                            (points[1].x, points[1].y, points[1].z),
                            (points[2].x, points[2].y, points[2].z),
                            (points[3].x, points[3].y, points[3].z)]
            
            targetPointsFound = False
            for targetPoints in targetPointsList:
                if pointTuples[0] in targetPoints and \
                        pointTuples[1] in targetPoints and \
                        pointTuples[2] in targetPoints and \
                        pointTuples[3] in targetPoints:    # all points equal
                    
                    #check order
                    index = targetPoints.index(pointTuples[0])
                    self.assertEqual(targetPoints.index(pointTuples[1]),
                                     (index + 1) % 4, 'points in wrong order')
                    targetPointsFound = True
                    break
            
            self.assertTrue(targetPointsFound,
                            'No corresponding points group found for polygon')
    
    
    def testStartPosition(self):
        grid = [['s']]
        
        gridMap = GridMap(None, grid)
        gridMap.edgeLength = 1
        
        position = gridMap.getStartPosition()
        self.assertEqual(position.x, 0.5)
        self.assertEqual(position.z, 0.5)
    
    def testStartPosition2(self):
        grid = [[1, 's']]
        
        gridMap = GridMap(None, grid)
        gridMap.edgeLength = 1
        
        position = gridMap.getStartPosition()
        self.assertEqual(position.x, 1.5)
        self.assertEqual(position.z, 0.5)
                


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()