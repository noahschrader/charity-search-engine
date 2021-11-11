import dataclasses
import requests

base_url = 'https://api.data.charitynavigator.org/v2'


def get_organizations(dto):
    response = requests.get(base_url + '/Organizations', dataclasses.asdict(dto))
    return response.json() if response.status_code == 200 else {}
