from typing import List
from unittest.mock import MagicMock, patch

import requests
from django.test import TestCase

from application.fema.FEMA import ApiQuery, Filter, ApiHandler, DisasterQuery


class TestApiHandler(TestCase):

    # Methods of this class should be patched as needed.
    class TestQuery(ApiQuery):

        def get_version(self):
            pass

        def get_entity_name(self):
            pass

        def handle_json_api_response(self, json):
            pass

        def build_query(self):
            return ""

        def add_filter(self, filter: Filter):
            pass

        def get_filters(self) -> List:
            pass

    def setUp(self) -> None:
        super().setUp()
        self.handler = ApiHandler()

    def test_return_none_on_bad_query(self):
        ok_response = MagicMock(ok=False)
        query = self.TestQuery()
        with patch.object(requests, "get", return_value=ok_response):
            self.assertIsNone(self.handler.query(query))

    def test_default_record_count(self):
        query = DisasterQuery()
        data = self.handler.query(query)
        self.assertLessEqual(len(data), ApiQuery.DEFAULT_RECORD_COUNT)

    def test_arbitrary_record_count(self):
        count = 12
        data = self.handler.query(DisasterQuery(), count)
        self.assertLessEqual(len(data), count)

    def test_max_record_count(self):
        count = ApiQuery.MAX_RECORD_COUNT
        data = self.handler.query(DisasterQuery(), count)
        self.assertGreater(len(data), ApiQuery.DEFAULT_RECORD_COUNT)
