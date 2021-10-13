from django.test import TestCase
from unittest.mock import patch # May need these for external API testing.
import requests
from FEMA import ApiHandler, DisasterQuery, ApiQuery, DateFilter, Filter, DeclarationTypeFilter
from datetime import datetime


class CharityNavigatorApi(TestCase):
    def testGetRequest(self):
        query = {'app_id': '998e64be', 'app_key': 'c99ca3e66a3f61b839486371709a0cd4'}
        response = requests.get('https://api.data.charitynavigator.org/v2/Organizations', query)
        data = response.json()
        self.assertTrue(data)


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

    def setUp(self) -> None:
        super().setUp()
        self.disaster_query = DisasterQuery()

    def test_preset_version_and_entity_name(self):
        self.assertEqual(self.disaster_query.get_version(), self.disaster_query.VERSION)
        self.assertEqual(self.disaster_query.get_entity_name(), self.disaster_query.ENTITY_NAME)

    def test_basic_query_string(self):
        expected_query_string = self.disaster_query.BASE_API_URI +\
                                "/" + self.disaster_query.VERSION +\
                                "/" + self.disaster_query.ENTITY_NAME
        self.assertEqual(self.disaster_query.build_query_string(), expected_query_string)

    def test_single_filtered_query_string(self):
        filter = DateFilter(DateFilter.LogicalOperator.GREATER_THAN, datetime(2021, 8, 1))
        self.disaster_query.add_filter(filter)
        expected_query_string = "{}/{}/{}{}{}{}{}".format(ApiQuery.BASE_API_URI,
                                                          DisasterQuery.VERSION,
                                                          DisasterQuery.ENTITY_NAME,
                                                          ApiQuery.PATH_QUERY_SEPARATOR,
                                                          Filter.COMMAND_STRING,
                                                          ApiQuery.QUERY_ASSIGNMENT_OPERATOR,
                                                          filter.build_filter_string())
        self.assertEqual(expected_query_string, self.disaster_query.build_query_string())

    def test_multi_filtered_qeury_string(self):
        filter_1 = DateFilter(Filter.LogicalOperator.GREATER_THAN, datetime(2012, 4, 7))
        # filter_2 = DeclarationTypeFilter()


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
        type = DeclarationTypeFilter.DeclarationType.MAJOR_DISASTER
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
    #     type = DisasterQuery.DeclarationType.EMERGENCY
    #     query = DisasterQuery(type, start_date)
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

