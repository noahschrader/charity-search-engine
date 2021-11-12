from enum import Enum
from dataclasses import dataclass

app_id = '998e64be'
app_key = 'c99ca3e66a3f61b839486371709a0cd4'


class SearchType(Enum):
    DEFAULT = 'DEFAULT'
    NAME_ONLY = 'NAME_ONLY'


class ScopeType(Enum):
    ALL = 'ALL'
    REGIONAL = 'REGIONAL'
    NATIONAL = 'NATIONAL'
    INTERNATIONAL = 'INTERNATIONAL'


class SortType(Enum):
    RELEVANCE = 'RELEVANCE:DESC'
    RATING = 'RATING:DESC'
    NAME = 'NAME:ASC'


filters = {'searchType': list(SearchType), 'scopeType': list(ScopeType), 'sortType': list(SortType)}


@dataclass
class CharityNavigatorDto:
    city: str
    state: str
    zip: int
    search: str
    searchType: SearchType
    scope: ScopeType
    app_id: str = app_id
    app_key: str = app_key
    pageSize: int = 25
    sort: SortType = SortType.RELEVANCE.value
    rated: int = 1
    pageNum: int = 1
