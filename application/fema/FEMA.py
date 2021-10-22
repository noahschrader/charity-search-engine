
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
    def build_query_string(self) -> str:
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

    def get_version(self):
        return self.VERSION

    def get_entity_name(self):
        return "DisasterDeclarationsSummaries"

    def handle_json_api_response(self, json):

        """
        Handles a response from a query of this ApiQuery.
        :param json: The JSON response given by a FEMA API endpoint.
        :return: A set of JSON disaster summaries which can be accessed using this classes Fields.
        """

        disasters = json[self.ENTITY_NAME]
        return disasters

    def build_query_string(self):
        query_str = self.BASE_API_URI + "/" + self.get_version() + "/" + self.get_entity_name()
        if len(self.filters) > 0:
            query_str += ApiQuery.PATH_QUERY_SEPARATOR + Filter.COMMAND_STRING + ApiQuery.ASSIGNMENT_OPERATOR
            for i, filter in enumerate(self.filters):
                query_str += filter.build_filter_string()
                if i < (len(self.filters) - 1):
                    query_str += " " + Filter.LogicalOperator.AND.value + " "
        return query_str

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

        query_string = query.build_query_string()
        if ApiQuery.PATH_QUERY_SEPARATOR in query_string:
            query_string += ApiQuery.ARGUMENT_SEPARATOR
        else:
            query_string += ApiQuery.PATH_QUERY_SEPARATOR
        query_string += "$top=" + str(record_count)
        print("ApiHandler: querying :" + query_string)
        response = requests.get(query_string)
        if not response.ok:
            return None
        json_data = response.json()
        return query.handle_json_api_response(json_data)
