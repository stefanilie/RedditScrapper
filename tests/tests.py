# -*- coding: utf-8 -*-
import os
import sys
import mock
import unittest

MYDIR = os.path.dirname(__file__)
sys.path.append(os.path.join(MYDIR, "../scrapper/"))
import scrapper

class ScrapperTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_make_call_non_ascii(self):
        scrapperObj = scrapper.Scrapper()
        result = scrapperObj.make_call("¤©«±¶µ", 1495490048)
        self.assertEqual(result, False)

    def test_make_call(self):
        test_json = {
            "id": "1234123",
            "title": "This is a test title",
            "selftext": "Test is a test for testing tests.",
            "num_comments": 45,
            "created": 1495490048,
            "subreddit": "test",
            "comments": [
                "this is the first comment",
                "this is the second commment",
                "this is the third comment"
            ]
        }
        mock_reddit = mock.patch("scrapper.Scrapper.reddit.subreddit").start()
        mock_insert = mock.patch("scrapper.Scrapper.insert_submission").start()
        mock_insert_comment = mock.patch("scrapper.Scrapper.insert_comment").start()
        mock_reddit.return_value = test_json
        mock_insert.return_value = "6ejt4t"
        mock_insert_comment.return_value = "3fas4gr"
        scrapperObj = scrapper.Scrapper()
        result = scrapperObj.make_call("python", 1495490048)
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
    #
    # """
    # ToDo: Create tests for flask module
    # """
    # def test_flask_stage_one(self):
    #     assertTrue(True)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(ScrapperTestCase, "test"))
    return test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
