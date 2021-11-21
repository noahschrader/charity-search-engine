from django.test import TestCase

from application.api.FEMA import Filter, DisasterQuery


class TestDisasterQuery(TestCase):

    class TestFilter(Filter):

        def __init__(self, filter_string: str):
            self.filter_string = filter_string

        def build_filter_string(self) -> str:
            return self.filter_string

    def setUp(self) -> None:
        super().setUp()
        self.disaster_query = DisasterQuery()

    def test_preset_version_and_entity_name(self):
        self.assertEqual(self.disaster_query.get_version(), self.disaster_query.VERSION)
        self.assertEqual(self.disaster_query.get_entity_name(), self.disaster_query.ENTITY_NAME)

    def test_basic_query(self):
        expected_query = {}
        self.assertEqual(expected_query, self.disaster_query.build_query())

    def test_single_filtered_query(self):
        query_filter = self.TestFilter("This is a test")
        self.disaster_query.add_filter(query_filter)
        expected_query = {
            Filter.COMMAND_STRING: query_filter.build_filter_string(),
        }
        self.assertEqual(expected_query, self.disaster_query.build_query())

    def test_multiple_filtered_query(self):
        filter_1 = self.TestFilter("This is filter_1")
        filter_2 = self.TestFilter("This is filter_2")
        self.disaster_query.add_filter(filter_1)
        self.disaster_query.add_filter(filter_2)
        filter_string = filter_1.build_filter_string() + " " + str(Filter.LogicalOperator.AND.value) + " " + filter_2.build_filter_string()
        expected_query = {
            Filter.COMMAND_STRING: filter_string,
        }
        self.assertEqual(expected_query, self.disaster_query.build_query())

    def test_filters_getter(self):
        query = DisasterQuery()
        query_filter = self.TestFilter("")
        query.add_filter(query_filter)
        filters = query.get_filters()
        self.assertEqual(1, len(filters))
        self.assertEqual(query_filter, filters[0])
