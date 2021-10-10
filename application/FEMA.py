
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

import requests
import abc
from datetime import datetime


class Filter(abc.ABC):

    COMMAND_STRING = "$filter"

    class LogicalOperator:
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

    DATA_FIELD = "incidentBeginDate"

    def __init__(self, operator: Filter.LogicalOperator, date: datetime):
        self.operator = operator
        self.date = date

    def build_filter_string(self) -> str:
        return "{} {} '{}'".format(self.DATA_FIELD, self.operator, self.date)

    def get_operator(self) -> Filter.LogicalOperator:
        return self.operator

    def get_date(self) -> datetime:
        return self.date


# Query entities and versions found at https://www.fema.gov/about/openfema/data-sets.
class ApiQuery(abc.ABC):

    BASE_API_URI = "https://www.fema.gov/api/open"
    PATH_QUERY_SEPARATOR = "?"
    QUERY_ASSIGNMENT_OPERATOR = "="

    @abc.abstractmethod
    def get_version(self):
        pass

    @abc.abstractmethod
    def get_entity_name(self):
        pass

    @abc.abstractmethod
    def handle_json_api_response(self, json: str):
        pass

    @abc.abstractmethod
    def build_query_string(self):
        pass

    @abc.abstractmethod
    def add_filter(self, filter: Filter):
        pass


class DisasterQuery(ApiQuery):

    VERSION = "v2"
    ENTITY_NAME = "DisasterDeclarationsSummaries"

    class Field:
        DECLARATION_TYPE = "declarationType"
        DECLARATION_TITLE = "declarationTitle"
        INCIDENT_BEGIN_DATE = "incidentBeginDate"

    class DeclarationType:
        EMERGENCY = "EM"
        FIRE_MANAGEMENT = "FM"
        MAJOR_DISASTER = "DR"

    def __init__(self, declaration_type: DeclarationType = None, start_date: datetime = None):

        """
        :param declaration_type: Queries disasters that are of a specific type. Different types are defined in
                                 DisasterQuery.DeclarationType.
        :param start_date: Filters the query to disasters that occurred after a given datetime.
        """

        self.declaration_type = declaration_type
        self.start_date = start_date

    def get_version(self):
        return self.VERSION

    def get_entity_name(self):
        return "DisasterDeclarationsSummaries"

    def handle_json_api_response(self, json: str):

        """
        Handles a response from a query of this ApiQuery.
        :param json: The JSON response given by a FEMA API endpoint.
        :return: A set of JSON disaster summaries which can be accessed using this classes Fields.
        """

        disasters = json["DisasterDeclarationsSummaries"]
        return disasters

    def build_query_string(self):
        query_str = self.BASE_API_URI + "/" + self.get_version() + "/" + self.get_entity_name()
        if self.start_date is not None:
            date_filter_str = self.generate_date_filter_str(self.start_date)
            query_str = self.add_filter_to_query(query_str, date_filter_str)
        if self.declaration_type is not None:
            declaration_type_filter_str = self.generate_declaration_type_filter_str(self.declaration_type)
            query_str = self.add_filter_to_query(query_str, declaration_type_filter_str)
        print("built query string: " + query_str)
        return query_str

    def add_filter_to_query(self, query_str: str, filter_str: str) -> str:
        updated_query_str = query_str
        if not self.filter_present(updated_query_str):
            updated_query_str += self.PATH_QUERY_SEPARATOR + "$filter" + self.QUERY_ASSIGNMENT_OPERATOR
        else:
            updated_query_str += " and "
        updated_query_str += filter_str
        return updated_query_str

    def filter_present(self, query_str: str) -> bool:
        if "$filter=" in query_str:
            return True
        return False

    def generate_date_filter_str(self, date: datetime) -> str:
        date_filter = "incidentBeginDate gt '" + str(date) + "'"
        return date_filter

    def generate_declaration_type_filter_str(self, declaration_type : DeclarationType):
        type_filter = "declarationType eq '{declaration_type}'".format(declaration_type=declaration_type)
        return type_filter

    def add_filter(self, filter: Filter):
        pass



class ApiHandler:

    def query(self, query: ApiQuery):

        """
        Queries the FEMA API using the given ApiQuery object.

        :returns: the result of query's handler_api_response() call or None if a response was not recieved.
        """

        if not isinstance(query, ApiQuery):
            raise TypeError("query is not a subclass of ApiQuery")
        query_string = query.build_query_string()
        response = requests.get(query_string)
        if not response.ok:
            return None
        json_data = response.json()
        return query.handle_json_api_response(json_data)
