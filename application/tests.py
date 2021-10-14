from typing import Final

from django.test import TestCase
from application.api.charity_navigator import get_organizations
from unittest.mock import patch # May need these for external API testing.
import requests
from FEMA import ApiHandler, DisasterQuery, ApiQuery, DateFilter, Filter, DeclarationTypeFilter
from datetime import datetime


class CharityNavigatorApi(TestCase):
    def testGetRequest(self):
        query = get_organizations({})
        self.assertIsNotNone(query)


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


class TestDisasterQuery(TestCase):

    class TestFilter(Filter):

        def __init__(self, filter_string: str):
            self.filter_string = filter_string

        def build_filter_string(self) -> str:
            return self.filter_string

    def build_basic_expected_query_string(self, query_obj: DisasterQuery):
        return self.disaster_query.BASE_API_URI +\
                                "/" + self.disaster_query.VERSION +\
                                "/" + self.disaster_query.ENTITY_NAME

    def setUp(self) -> None:
        super().setUp()
        self.disaster_query = DisasterQuery()

    def test_preset_version_and_entity_name(self):
        self.assertEqual(self.disaster_query.get_version(), self.disaster_query.VERSION)
        self.assertEqual(self.disaster_query.get_entity_name(), self.disaster_query.ENTITY_NAME)

    def test_basic_query_string(self):
        expected_query_string = self.build_basic_expected_query_string(self.disaster_query)
        self.assertEqual(self.disaster_query.build_query_string(), expected_query_string)

    def test_single_filtered_query_string(self):
        filter = self.TestFilter("This is a test")
        self.disaster_query.add_filter(filter)
        expected_query_string = self.build_basic_expected_query_string(self.disaster_query) +\
                                ApiQuery.PATH_QUERY_SEPARATOR +\
                                Filter.COMMAND_STRING +\
                                ApiQuery.QUERY_ASSIGNMENT_OPERATOR +\
                                filter.build_filter_string()
        self.assertEqual(expected_query_string, self.disaster_query.build_query_string())

    def test_multiple_filtered_query_strings(self):
        filter_1 = self.TestFilter("This is filter_1")
        filter_2 = self.TestFilter("This is filter_2")
        self.disaster_query.add_filter(filter_1)
        self.disaster_query.add_filter(filter_2)
        expected_query_string = self.build_basic_expected_query_string(self.disaster_query) + \
                                ApiQuery.PATH_QUERY_SEPARATOR + \
                                Filter.COMMAND_STRING + \
                                ApiQuery.QUERY_ASSIGNMENT_OPERATOR + \
                                filter_1.build_filter_string() +\
                                " " + Filter.LogicalOperator.AND.value + " " +\
                                filter_2.build_filter_string()
        self.assertEqual(expected_query_string, self.disaster_query.build_query_string())

class TestDateFilter(TestCase):

    def test_getters(self):
        o = DateFilter.LogicalOperator.EQUAL
        d = datetime(2000, 1, 1)
        df = DateFilter(o, d)
        self.assertEqual(df.get_operator(), o)
        self.assertEqual(df.get_date(), d)

    def test_build_string(self):
        date_filter = DateFilter(DateFilter.LogicalOperator.GREATER_THAN, datetime(2021, 8, 1))
        expected_string = "{} {} '{}'".format(date_filter.DATA_FIELD, date_filter.get_operator(), date_filter.get_date())
        self.assertEqual(date_filter.build_filter_string(), expected_string)


class TestDeclarationTypeFilter(TestCase):

    def test_query_string(self):
        for type in DeclarationTypeFilter.DeclarationType:
            dtf = DeclarationTypeFilter(type)
            expected_filter_string = "{field} {equals} {type}".format(field=dtf.DATA_FIELD,
                                                                      equals=Filter.LogicalOperator.EQUAL.value,
                                                                      type=type.value)
            self.assertEqual(expected_filter_string, dtf.build_filter_string())


class FemaApi(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.handler = ApiHandler()

    # def test_demo(self):
    #     start_date = datetime(2021, 8, 1)
    #     type = DeclarationTypeFilter.DeclarationType.EMERGENCY
    #     query = DisasterQuery()
    #     query.add_filter(DateFilter(Filter.LogicalOperator.GREATER_THAN, start_date))
    #     query.add_filter(DeclarationTypeFilter(type))
    #     data = self.handler.query(query)
    #     for disaster in data:
    #         print(
    #             "[" +
    #             disaster[DisasterQuery.Field.DECLARATION_TITLE] +
    #             ", " +
    #             disaster[DisasterQuery.Field.DECLARATION_TYPE] +
    #             ", " +
    #             disaster[DisasterQuery.Field.INCIDENT_BEGIN_DATE] +
    #             "]"
    #         )

