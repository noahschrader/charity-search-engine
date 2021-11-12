from datetime import datetime

from django.test import TestCase

from application.fema.FEMA import DateFilter


class TestDateFilter(TestCase):

    def test_getters(self):
        o = DateFilter.LogicalOperator.EQUAL
        d = datetime(2000, 1, 1)
        df = DateFilter(o, d)
        self.assertEqual(df.get_operator(), o)
        self.assertEqual(df.get_date(), d)

    def test_build_string(self):
        date_filter = DateFilter(DateFilter.LogicalOperator.GREATER_THAN, datetime(2021, 8, 1))
        expected_string = "{} {} '{}'".format(date_filter.DATA_FIELD, date_filter.get_operator().value, date_filter.get_date())
        self.assertEqual(expected_string, date_filter.build_filter_string())
