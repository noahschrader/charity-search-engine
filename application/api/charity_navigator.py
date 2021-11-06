from enum import Enum

import requests

app_id = '998e64be'
app_key = 'c99ca3e66a3f61b839486371709a0cd4'

base_url = 'https://api.data.charitynavigator.org/v2'
base_query = {'app_id': app_id, 'app_key': app_key, 'pageSize': 25, "rated": "TRUE"}


class SortType(Enum):
    RATING = {
        "sort": "RATING:DESC"
    }

    NAME = {
        "sort": "NAME:ASC"
    }

    RELEVANCE = {
        "sort": "RELEVANCE:DESC"
    }


def get_organizations(query, sort=SortType.RATING):
    query.update(base_query)
    query.update(sort.value)
    response = requests.get(base_url + '/Organizations', query)
    return response.json() if response.status_code == 200 else {}
