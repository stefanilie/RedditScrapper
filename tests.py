import unittest
from mock import MagicMock

import scrapper

class TestFunctions:
    def test_index_comments(self):
        self.db_conn = MagicMock()
        scrapper.Scrapper.index_comments()
        self.db_conn.assertCalledWith()
