from django.test import TestCase
import requests


class CharityNavigatorApi(TestCase):
    def testGetRequest(self):
        query = {'app_id': '998e64be', 'app_key': 'c99ca3e66a3f61b839486371709a0cd4'}
        response = requests.get('https://api.data.charitynavigator.org/v2/Organizations', query)
        data = response.json()
        self.assertTrue(data)
