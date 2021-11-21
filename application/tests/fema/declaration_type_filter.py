from django.test import TestCase

from application.api.FEMA import DeclarationTypeFilter, Filter


class TestDeclarationTypeFilter(TestCase):

    def test_query_string(self):
        for type in DeclarationTypeFilter.DeclarationType:
            dtf = DeclarationTypeFilter(type)
            expected_filter_string = "{field} {equals} '{type}'".format(field=dtf.DATA_FIELD,
                                                                      equals=Filter.LogicalOperator.EQUAL.value,
                                                                      type=type.value)
            self.assertEqual(expected_filter_string, dtf.build_filter_string())
