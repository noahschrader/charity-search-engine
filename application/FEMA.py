# Datasets found at https://www.fema.gov/about/openfema/data-sets.
# These are what will be used as "entities"

import requests

class ApiData:

    def __init__(self, data):
        self.data = data

    def get_data(self):
        return self.data


class ApiHandler:

    BASE_URI = "https://www.fema.gov/api/open"

    def query(self, version, entity) -> ApiData:
        query_string = self.__build_query_string(version, entity)
        r = requests.get(query_string)
        data = r.json()
        return ApiData(data)

    def __build_query_string(self, version, entity):
        return self.BASE_URI + "/" + version + "/" + entity