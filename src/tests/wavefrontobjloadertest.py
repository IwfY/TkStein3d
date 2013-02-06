import unittest
from engine.server.wavefrontobjloader import WavefrontObjLoader


class WavefrontObjLoaderTest(unittest.TestCase):


    def testSimplest(self):
        objLoader = WavefrontObjLoader('testdata/test.obj')
        polygons = objLoader.getPolygons()
        self.assertEqual(len(polygons), 1)
        
        polygon = polygons[0]
        self.assertEqual(len(polygon.points), 3)
        
        point0 = polygon.points[0]
        self.assertEqual(point0.x, 0.0)
        self.assertEqual(point0.y, 0.0)
        self.assertEqual(point0.z, 1.0)
        
        point2 = polygon.points[2]
        self.assertEqual(point2.x, 1.0)
        self.assertEqual(point2.y, 1.0)
        self.assertEqual(point2.z, 1.0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()