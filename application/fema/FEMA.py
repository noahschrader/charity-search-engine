
"""
For disasters: https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2#
The handler should be able to return a disaster object which can give us
basic info that we need for charity filters. At least disaster name.

Potential Disaster fields of interest for charities:
- declarationTitle
- incidentType
-

DataSet -> ApiHandler -> List

FEMA time format:
YYYY-MM-DDTHH:MM:SS.mmmz

"""
import typing
from enum import Enum
from typing import Final, List

import requests
import abc
from datetime import datetime


class Filter(abc.ABC):

    COMMAND_STRING: Final = "$filter"

    class LogicalOperator(Enum):
        EQUAL = "eq"
        NOT_EQUAL = "ne"
        GREATER_THAN = "gt"
        GREATER_THAN_OR_EQUAL = "ge"
        LESS_THAN = "lt"
        LESS_THAN_OR_EQUAL = "le"
        AND = "and"
        OR = "or"
        NOT = "not"

    @abc.abstractmethod
    def build_filter_string(self) -> str:
        pass


class DateFilter(Filter):

    DATA_FIELD: Final = "incidentBeginDate"

    def __init__(self, operator: Filter.LogicalOperator, date: datetime):
        self.operator = operator
        self.date = date

    def build_filter_string(self) -> str:
        return "{} {} '{}'".format(self.DATA_FIELD, self.operator.value, self.date)

    def get_operator(self) -> Filter.LogicalOperator:
        return self.operator

    def get_date(self) -> datetime:
        return self.date


# Query entities and versions found at https://www.fema.gov/about/openfema/data-sets.
class ApiQuery(abc.ABC):

    BASE_API_URI: Final = "https://www.fema.gov/api/open"
    PATH_QUERY_SEPARATOR: Final = "?"
    ASSIGNMENT_OPERATOR: Final = "="
    ARGUMENT_SEPARATOR = "&"
    DEFAULT_RECORD_COUNT = 1000
    MAX_RECORD_COUNT = -1

    @abc.abstractmethod
    def get_version(self) -> str:
        pass

    @abc.abstractmethod
    def get_entity_name(self) -> str:
        pass

    @abc.abstractmethod
    def handle_json_api_response(self, json: str) -> typing.Dict:
        pass

    @abc.abstractmethod
    def build_query(self) -> typing.Dict:
        pass

    @abc.abstractmethod
    def add_filter(self, filter: Filter):
        pass

    @abc.abstractmethod
    def get_filters(self) -> List:
        pass


class DisasterQuery(ApiQuery):

    VERSION: Final = "v2"
    ENTITY_NAME: Final = "DisasterDeclarationsSummaries"

    class Field(Enum):
        DECLARATION_TYPE = "declarationType"
        DECLARATION_TITLE = "declarationTitle"
        INCIDENT_BEGIN_DATE = "incidentBeginDate"

    def __init__(self):
        super()
        self.filters = []

    def get_version(self) -> str:
        return self.VERSION

    def get_entity_name(self) -> str:
        return self.ENTITY_NAME

    def handle_json_api_response(self, json):

        """
        Handles a response from a query of this ApiQuery.
        :param json: The JSON response given by a FEMA API endpoint.
        :return: A set of JSON disaster summaries which can be accessed using this classes Fields.
        """

        disasters = json[self.ENTITY_NAME]
        return disasters

    def build_query(self) -> typing.Dict:
        combined_filter_string = ""

        for i, fltr in enumerate(self.filters):
            combined_filter_string += fltr.build_filter_string()
            if i < len(self.filters) - 1:
                combined_filter_string += " " + Filter.LogicalOperator.AND.value + " "

        query = {
            Filter.COMMAND_STRING: combined_filter_string
        }

        return query

    def add_filter(self, filter: Filter):
        self.filters.append(filter)

    def get_filters(self) -> List:
        return self.filters


class DeclarationTypeFilter(Filter):

    DATA_FIELD: Final = "declarationType"

    class DeclarationType(Enum):
        EMERGENCY = "EM"
        FIRE_MANAGEMENT = "FM"
        MAJOR_DISASTER = "DR"

    def __init__(self, type: DeclarationType):
        self.d_type = type

    def build_filter_string(self) -> str:
        query_string = "{} {} '{}'".format(self.DATA_FIELD, Filter.LogicalOperator.EQUAL.value, self.d_type.value)
        return query_string


class ApiHandler:

    def query(self, query: ApiQuery, record_count=ApiQuery.DEFAULT_RECORD_COUNT):

        """
        Queries the FEMA API using the given ApiQuery object.

        :returns: the result of query's handler_api_response() call or None if a response was not recieved.
        """

        query_values = query.build_query()
        uri = "{base}/{v}/{e}".format(base=query.BASE_API_URI, v=query.get_version(), e=query.get_entity_name())
        json_data = self.page_through(uri, query_values, record_count)
        return json_data

    def page_through(self, url: str, query_values: typing.Dict, record_count: int) -> typing.Dict:
        total_count = self.get_total_record_count(url, query_values)
        print("Found total count: " + str(total_count))
        if total_count == -1:
            return None
        if record_count == ApiQuery.MAX_RECORD_COUNT:
            record_count = total_count
        full_count_iterations = int(record_count / 1001)
        data = []

        for i in range(full_count_iterations + 1):
            query_values["$skip"] = 1000 * i
            query_values["$top"] = min(record_count - query_values.get("$skip"), 1000)
            response = requests.get(url, query_values)
            print("Response url: " + str(response.url))
            if not response.ok:
                return None

            data.extend(response.json().get("DisasterDeclarationsSummaries"))

        return data

    def get_total_record_count(self, url, query_values) -> int:
        query_values_cpy = query_values.copy()
        query_values_cpy["$top"] = 1
        query_values_cpy["$inlinecount"] = "allpages"
        response = requests.get(url, query_values_cpy)
        if not response.ok:
            return -1
        return response.json().get("metadata").get("count")
