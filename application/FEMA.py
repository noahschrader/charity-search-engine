
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


# Query entities and versions found at https://www.fema.gov/about/openfema/data-sets.
class ApiQuery(abc.ABC):
    BASE_API_URI = "https://www.fema.gov/api/open"

    @abc.abstractmethod
    def get_version(self):
        pass

    @abc.abstractmethod
    def get_entity_name(self):
        pass

    @abc.abstractmethod
    def handle_api_response(self, json):
        pass

    @abc.abstractmethod
    def build_query_string(self):
        pass


class DisasterQuery(ApiQuery):

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
        return "v2"

    def get_entity_name(self):
        return "DisasterDeclarationsSummaries"

    def handle_api_response(self, json):

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

    def add_filter_to_query(self, query_str, filter_str) -> str:
        updated_query_str = query_str
        if not self.filter_present(updated_query_str):
            updated_query_str += "?$filter="
        else:
            updated_query_str += " and "
        updated_query_str += filter_str
        return updated_query_str

    def filter_present(self, query_str) -> bool:
        if "$filter=" in query_str:
            return True
        return False

    def generate_date_filter_str(self, date: datetime) -> str:
        date_filter = "incidentBeginDate gt '" + str(date) + "'"
        return date_filter

    def generate_declaration_type_filter_str(self, declaration_type : DeclarationType):
        type_filter = "declarationType eq '{declaration_type}'".format(declaration_type=declaration_type)
        return type_filter


class ApiHandler:

    def query(self, query: ApiQuery):

        """
        Queries the FEMA API using the given ApiQuery object.

        :returns: the result of query's handler_api_response() call
        """

        if not isinstance(query, ApiQuery):
            raise TypeError("query is not a subclass of ApiQuery")
        query_string = query.build_query_string()
        response = requests.get(query_string)
        json_data = response.json()
        return query.handle_api_response(json_data)
