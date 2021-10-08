from django.test import TestCase
import requests
from FEMA import ApiHandler, DisasterQuery
from datetime import datetime


class CharityNavigatorApi(TestCase):
    def testGetRequest(self):
        query = {'app_id': '998e64be', 'app_key': 'c99ca3e66a3f61b839486371709a0cd4'}
        response = requests.get('https://api.data.charitynavigator.org/v2/Organizations', query)
        data = response.json()
        self.assertTrue(data)


class FemaApi(TestCase):

    def setUp(self) -> None:
        self.handler = ApiHandler()

    def test_something_is_created_on_creation(self):
        query = DisasterQuery()
        self.assertIsNotNone(query)

    def test(self):
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

