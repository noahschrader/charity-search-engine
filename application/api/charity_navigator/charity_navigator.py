import dataclasses
import requests

base_url = 'https://api.data.charitynavigator.org/v2'


def get_organizations(dto):
    dto_dict = {k: v for k, v in dataclasses.asdict(dto).items() if v}
    response = requests.get(base_url + '/Organizations', dto_dict)
    return response.json() if response.status_code == 200 else {}
