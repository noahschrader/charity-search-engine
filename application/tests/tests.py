import datetime
from unittest import TestLoader

from django.test import TestCase
from application.api.charity_navigator import get_organizations
from application.views.home import lookup_recent_disaster_charities


class CharityNavigatorApi(TestCase):
    def testGetRequest(self):
        query = get_organizations({})
        self.assertIsNotNone(query)

class FEMAApi(TestCase):

    def test(self):
        lookup_recent_disaster_charities()


