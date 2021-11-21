from django.test import TestCase
from application.api.charity_navigator import get_organizations


class CharityNavigatorApi(TestCase):
    def testGetRequest(self):
        query = get_organizations({})
        self.assertIsNotNone(query)
