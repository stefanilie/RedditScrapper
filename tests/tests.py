# -*- coding: utf-8 -*-
import os
import sys
import unittest
from mock import MagicMock

MYDIR = os.path.dirname(__file__)
sys.path.append(os.path.join(MYDIR, "../scrapper/"))
import scrapper

class ScrapperTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_make_call(self):
        scrapperObj = scrapper.Scrapper()
        result = scrapperObj.make_call("¤©«±¶µ", 1495490048)
        self.assertEqual(result, False)

    def test_stage_one(self):
        scrapperObj = scrapper.Scrapper()
        self.assertFalse(scrapperObj.stage_one("subreddit", "string", 123442.123123))
        self.assertFalse(scrapperObj.stage_one("subr¤©«±¶µeddit", 1245522425, 1244546225))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    """
    ToDo: Create tests for flask module
    """
    def test_flask_stage_one(self):
        assertTrue(True)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(ScrapperTestCase, "test"))
    return test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
