import unittest
from handle_data import findCode, findStation, createGraph, findRoute, allRoutes, shortestRoute, printRoute

class TestHandleData(unittest.TestCase):
    # Unit test for findCode function
    def test_findCode(self):
        self.assertEqual(findCode('Bugis'), 'EW12/DT14')

    # Unit test for findStation function
    def test_findStation(self):
        self.assertEqual(findStation('NS22/TE14'), 'Orchard')

    # Unit test for printRoute function
    def test_printRoute(self):
        route = ['DT13', 'EW12/DT14']
        testRoute = printRoute(route)
        outRoute = [['Rochor', 'Bugis', {'DT'}]]
        self.assertEqual(testRoute, outRoute)