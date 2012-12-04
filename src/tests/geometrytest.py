'''
Created on Dec 4, 2012

@author: marcel
'''
import unittest
from engine.coordinate import Vector3D, Point3D
from engine.mathhelper import getVectorDotProduct, getAngleBetweenVectors
import math
from engine.polygon import Polygon


class Test(unittest.TestCase):


    def testDotProduct(self):
        vector1 = Vector3D(1, 1, 1)
        vector2 = Vector3D(-1, -1, -1)
        vector3 = Vector3D(1, -5, 0)
        
        result = getVectorDotProduct(vector1, vector1)        
        self.assertEqual(result, 3)
        
        result = getVectorDotProduct(vector1, vector2)        
        self.assertEqual(result, -3)
        
        result = getVectorDotProduct(vector1, vector3)        
        self.assertEqual(result, -4)
        
    
    def testCrossProduct(self):
        vector1 = Vector3D(1, 1, 1)
        vector2 = Vector3D(-1, -1, -1)
        vector3 = Vector3D(1, -5, 0)
        vector4 = Vector3D(1, 0, 0)
        vector5 = Vector3D(0, 1, 0)
        vector6 = Vector3D(0, 0, 1)
        
        result = vector1.getCrossProduct(vector1)        
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 0)
        self.assertEqual(result.z, 0)
        
        result = vector1.getCrossProduct(vector2)        
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 0)
        self.assertEqual(result.z, 0)
        
        result = vector1.getCrossProduct(vector3)        
        self.assertEqual(result.x, 5)
        self.assertEqual(result.y, 1)
        self.assertEqual(result.z, -6)
        
        result = vector4.getCrossProduct(vector5)        
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 0)
        self.assertEqual(result.z, 1)
        
        result = vector4.getCrossProduct(vector6)        
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, -1)
        self.assertEqual(result.z, 0)
        
        result = vector6.getCrossProduct(vector4)        
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 1)
        self.assertEqual(result.z, 0)
    
    def testGetAngleBetweenVectors(self):
        vector1 = Vector3D(1, 0, 0)
        vector2 = Vector3D(0, 1, 0)
        vector3 = Vector3D(0, 0, 1)
        vector4 = Vector3D(0, 0, -1)
        
        result = getAngleBetweenVectors(vector1, vector1)
        self.assertEqual(result, 0.0)
        
        result = getAngleBetweenVectors(vector1, vector2)
        self.assertEqual(result, math.pi / 2)
        
        result = getAngleBetweenVectors(vector3, vector4)
        self.assertEqual(result, math.pi)
    
    
    def testPolygonNormal(self):
        p1 = Point3D(0, 0, 0)
        p2 = Point3D(1, 0, 0)
        p3 = Point3D(1, 1, 0)
        p4 = Point3D(0, 1, 0)
        
        p5 = Point3D(1, 0, 1)
        p6 = Point3D(0, 0, 1)
        
        polygon1 = Polygon('', [p1, p2, p3, p4])
        polygon2 = Polygon('', [p1, p2, p5, p6])
        
        result = polygon1.getNormalVector()     
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 0)
        self.assertEqual(result.z, -1)
        
        result = polygon2.getNormalVector()     
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 1)
        self.assertEqual(result.z, 0)
        
    
    def testPolygonFacesPoint(self):
        p1 = Point3D(0, 0, 0)
        p2 = Point3D(1, 0, 0)
        p3 = Point3D(1, 1, 0)
        p4 = Point3D(0, 1, 0)
        
        p5 = Point3D(1, 0, 1)
        p6 = Point3D(0, 0, 1)
        
        p7 = Point3D(0, 1, 1)
        p8 = Point3D(0, 1, 0)
        
        polygon1 = Polygon('', [p1, p2, p3, p4])
        polygon2 = Polygon('', [p1, p2, p5, p6])
        polygon3 = Polygon('', [p1, p6, p7, p8])
        
        t1 = Point3D(0, 0, -1)
        t2 = Point3D(0, 0, 1)
        t3 = Point3D(0.5, 0.5, 0)
        t4 = Point3D(0, 1, 0)
        t5 = Point3D(1, 0, 0)
        
        result = polygon1.polygonFacesPoint(t1)
        self.assertTrue(result)
        
        result = polygon1.polygonFacesPoint(t2)
        self.assertFalse(result)
        
        result = polygon1.polygonFacesPoint(t3)
        self.assertTrue(result)
        
        result = polygon2.polygonFacesPoint(t4)
        self.assertTrue(result)
        
        result = polygon3.polygonFacesPoint(t5)
        self.assertTrue(result)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAngleBetweenAngles']
    unittest.main()
