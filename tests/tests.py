# -*- coding: utf-8 -*-
import os
import sys
import mock
import unittest

from mock import patch

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
        test_json = [{
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
            }]

        scrapper_call = scrapper.Scrapper()
        mock_subreddit = mock.MagicMock()
        # mocking the submissions part of the subreddits call.
        mock_subreddit.submissions.return_value = test_json
        scrapper_call.reddit.subreddit = mock.MagicMock().side_effect = mock_subreddit
        result = scrapper_call.make_call("python", 1495490048)

        self.assertEqual(result, True)

    def test_stage_one_false(self):
        scrapper_call = scrapper.Scrapper()
        self.assertFalse(scrapper_call.stage_one("subreddit", "string", 123442.123123))
        self.assertFalse(scrapper_call.stage_one("subr¤©«±¶µeddit", 1245522425, 1244546225))

    def test_stage_no_kwd(self):
        submissions_json = [{
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
        }]
        comments_json = [{
            "id": "1234123",
            "body": "Test",
            "sub_id": "Test",
            "subreddit": "python",
            "created": "123"
        }]

        scrapper_call = scrapper.Scrapper()
        mock_comments = mock.MagicMock()
        mock_comments.find.return_value = comments_json
        mock_submissions = mock.MagicMock()
        mock_submissions.find.return_value = submissions_json
        scrapper_call.db_conn.Submissions = mock.MagicMock().side_effect = mock_submissions
        scrapper_call.db_conn.Comments = mock.MagicMock().side_effect = mock_comments
        result = scrapper_call.stage_one("subreddit", 1245522425, 1244546225)

        self.assertTrue(result)

    def test_stage(self):
        submissions_json = [{
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
        }]
        comments_json = [{
            "id": "1234123",
            "body": "Test",
            "sub_id": "Test",
            "subreddit": "python",
            "created": "123"
        }]

        scrapper_call = scrapper.Scrapper()
        c = mock.MagicMock()
        c.find.return_value = comments_json
        s = mock.MagicMock()
        s.find.return_value = submissions_json
        scrapper_call.db_conn.Submissions = mock.MagicMock().side_effect = s
        scrapper_call.db_conn.Comments = mock.MagicMock().side_effect = c
        result = scrapper_call.stage_one("subreddit", 1245522425, 1244546225, "test")

        self.assertTrue(result)

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
