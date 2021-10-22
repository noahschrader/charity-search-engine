from django.test import TestCase
from application.api.charity_navigator import get_organizations
from application.fema.FEMA import ApiHandler, DisasterQuery, ApiQuery, DateFilter, Filter, DeclarationTypeFilter
from datetime import datetime


class CharityNavigatorApi(TestCase):
    def testGetRequest(self):
        query = get_organizations({})
        self.assertIsNotNone(query)


class FemaApi(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.handler = ApiHandler()

    def test_demo(self):
        start_date = datetime(2021, 8, 1)
        type = DeclarationTypeFilter.DeclarationType.EMERGENCY
        query = DisasterQuery()
        query.add_filter(DateFilter(Filter.LogicalOperator.GREATER_THAN, start_date))
        query.add_filter(DeclarationTypeFilter(type))
        data = self.handler.query(query)
        for disaster in data:
            print(
                "[" +
                disaster[DisasterQuery.Field.DECLARATION_TITLE.value] +
                ", " +
                disaster[DisasterQuery.Field.DECLARATION_TYPE.value] +
                ", " +
                disaster[DisasterQuery.Field.INCIDENT_BEGIN_DATE.value] +
                "]"
            )

