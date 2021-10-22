from django.test import TestCase

from application.fema.FEMA import Filter, DisasterQuery, ApiQuery


class TestDisasterQuery(TestCase):

    class TestFilter(Filter):

        def __init__(self, filter_string: str):
            self.filter_string = filter_string

        def build_filter_string(self) -> str:
            return self.filter_string

    def build_basic_expected_query_string(self, query_obj: DisasterQuery):
        return query_obj.BASE_API_URI +\
                                "/" + query_obj.VERSION +\
                                "/" + query_obj.ENTITY_NAME

    def setUp(self) -> None:
        super().setUp()
        self.disaster_query = DisasterQuery()

    def test_preset_version_and_entity_name(self):
        self.assertEqual(self.disaster_query.get_version(), self.disaster_query.VERSION)
        self.assertEqual(self.disaster_query.get_entity_name(), self.disaster_query.ENTITY_NAME)

    def test_basic_query_string(self):
        expected_query_string = self.build_basic_expected_query_string(self.disaster_query)
        self.assertEqual(expected_query_string, self.disaster_query.build_query_string())

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
