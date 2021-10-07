
"""
For disasters: https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2#
The handler should be able to return a disaster object which can give us
basic info that we need for charity filters. At least disaster name.

Potential Disaster fields of interest for charities:
- declarationTitle
- incidentType
-

DataSet -> ApiHandler -> List<
"""

import requests
import abc


class DisasterData:
    def __init__(self, disaster_json):
        self.title = ""
        self.declaration_date = ""
        self.incident_type = ""
        pass

    def get_title(self):
        return self.title

    def get_declaration_date(self):
        return self.declaration_date

    def get_incident_type(self):
        return self.incident_type


# Query entities and versions found at https://www.fema.gov/about/openfema/data-sets.
class ApiQuery(abc.ABC):
    BASE_URI = "https://www.fema.gov/api/open"

    @abc.abstractmethod
    def get_version(self):
        pass

    @abc.abstractmethod
    def get_entity_name(self):
        pass


class DisasterQuery(ApiQuery):

    def get_version(self):
        return "v2"

    def get_entity_name(self):
        return "DisasterDeclarationsSummaries"


class ApiHandler:

    def query(self, query: ApiQuery):
        if not isinstance(query, ApiQuery):
            raise TypeError("query is not a subclass of ApiQuery")
        query_string = self.__build_query_string(query)
        r = requests.get(query_string)
        data = r.json()
        print(data)

    def __build_query_string(self, query):
        return query.BASE_URI + "/" + query.get_version() + "/" + query.get_entity_name()
