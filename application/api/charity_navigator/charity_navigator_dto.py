from enum import Enum
from dataclasses import dataclass

app_id = '998e64be'
app_key = 'c99ca3e66a3f61b839486371709a0cd4'


class SortType(Enum):
    RATING = 'RATING:DESC'
    NAME = 'NAME:ASC'
    RELEVANCE = 'RELEVANCE:DESC'


@dataclass
class CharityNavigatorDto:
    search: str
    app_id: str = app_id
    app_key: str = app_key
    pageSize: int = 25
    sort: SortType = SortType.RELEVANCE.value
    rated: int = 1
    pageNum: int = 1
