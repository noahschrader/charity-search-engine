from django.test import TestCase
import requests
from FEMA import ApiHandler, DisasterQuery


class CharityNavigatorApi(TestCase):
    def testGetRequest(self):
        query = {'app_id': '998e64be', 'app_key': 'c99ca3e66a3f61b839486371709a0cd4'}
        response = requests.get('https://api.data.charitynavigator.org/v2/Organizations', query)
        data = response.json()
        self.assertTrue(data)


class FemaApi(TestCase):
    def test(self):
        handler = ApiHandler()
        query = DisasterQuery(2021)
        data = handler.query(query)
        for stuff in data:
            print(stuff)
