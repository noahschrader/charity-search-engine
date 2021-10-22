import datetime

from django.test import TestCase
from application.api.charity_navigator import get_organizations
from application.fema.FEMA import ApiHandler, DisasterQuery, DateFilter, Filter, DeclarationTypeFilter


class CharityNavigatorApi(TestCase):
    def testGetRequest(self):
        query = get_organizations({})
        self.assertIsNotNone(query)

class FEMAApi(TestCase):

    def test(self):
        handler = ApiHandler()
        start_date = datetime.datetime(2020, 1, 1)
        query = DisasterQuery()
        #query.add_filter(DateFilter(Filter.LogicalOperator.GREATER_THAN_OR_EQUAL, start_date))
        data = handler.query(query, 4700)
        print("Record count: " + str(len(data)))
        # for datum in data:
        #     print(datum)
