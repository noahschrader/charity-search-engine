from django.test import TestCase
from unittest.mock import Mock, patch # May need these for external API testing.
import requests
from FEMA import ApiHandler, DisasterQuery, ApiQuery
from datetime import datetime


class CharityNavigatorApi(TestCase):
    def testGetRequest(self):
        query = {'app_id': '998e64be', 'app_key': 'c99ca3e66a3f61b839486371709a0cd4'}
        response = requests.get('https://api.data.charitynavigator.org/v2/Organizations', query)
        data = response.json()
        self.assertTrue(data)


class TestApiHandler(TestCase):

    class TestQuery(ApiQuery):

        def get_version(self):
            pass

        def get_entity_name(self):
            pass

        def handle_api_response(self, json):
            pass

        def build_query_string(self):
            pass

    def setUp(self) -> None:
        super().setUp()
        self.handler = ApiHandler()

    def test_init(self):
        self.assertIsNotNone(self.handler)

    def test_empty_query(self):
        with self.assertRaises(TypeError):
            self.handler.query()

    def test_bad_query_arg(self):
        with self.assertRaises(TypeError):
            self.handler.query(0)

    def test_blank_build_query_string(self):

        # This lets us choose the return value of build_query_String() to test when different urls are used.
        with patch.object(TestApiHandler.TestQuery, 'build_query_string', return_value="") as mock_method:
            with self.assertRaises(requests.exceptions.MissingSchema):
                self.handler.query(self.TestQuery())


class FemaApi(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.handler = ApiHandler()

    def test_something_is_created_on_creation(self):
        query = DisasterQuery()
        self.assertIsNotNone(query)

    def test_demo(self):
        start_date = datetime(2021, 8, 1)
        type = DisasterQuery.DeclarationType.EMERGENCY
        query = DisasterQuery(type, start_date)
        data = self.handler.query(query)
        for disaster in data:
            print(
                "[" +
                disaster[DisasterQuery.Field.DECLARATION_TITLE] +
                ", " +
                disaster[DisasterQuery.Field.DECLARATION_TYPE] +
                ", " +
                disaster[DisasterQuery.Field.INCIDENT_BEGIN_DATE] +
                "]"
            )

