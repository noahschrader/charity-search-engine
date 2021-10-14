import requests

app_id = '998e64be'
app_key = 'c99ca3e66a3f61b839486371709a0cd4'

base_url = 'https://api.data.charitynavigator.org/v2'
base_query = {'app_id': app_id, 'app_key': app_key, 'pageSize': 25, 'pageNum': 1, 'sort': 'RATING:DESC'}


def get_organizations(query):
    query.update(base_query)
    response = requests.get(base_url + '/Organizations', query)
    return response.json()
