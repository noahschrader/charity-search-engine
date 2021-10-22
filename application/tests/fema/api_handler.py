from unittest.mock import MagicMock, patch

import requests
from django.test import TestCase

from application.fema.FEMA import ApiQuery, Filter, ApiHandler


class TestApiHandler(TestCase):

    # Methods of this class should be patched as needed.
    class TestQuery(ApiQuery):

        def get_version(self):
            pass

        def get_entity_name(self):
            pass

        def handle_json_api_response(self, json):
            pass

        def build_query_string(self):
            pass

        def add_filter(self, filter: Filter):
            pass

    def setUp(self) -> None:
        super().setUp()
        self.handler = ApiHandler()

    def test_return_none_on_bad_query(self):
        ok_response = MagicMock(ok=False)
        query = self.TestQuery()
        with patch.object(requests, "get", return_value=ok_response):
            self.assertIsNone(self.handler.query(query))
