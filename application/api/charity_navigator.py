import requests

app_id = '998e64be'
app_key = 'c99ca3e66a3f61b839486371709a0cd4'

base_url = 'https://api.data.charitynavigator.org/v2'
base_query = {'app_id': app_id, 'app_key': app_key, 'pageSize': 1000, 'pageNum': 1}


def get_organizations(query):
    query.update(base_query)
    response = requests.get(base_url + '/Organizations', query)
    data = response.json()
    while response.status_code == 200:
        query['pageNum'] += 1
        response = requests.get(base_url + '/Organizations', query)
        data += response.json()
    return data
