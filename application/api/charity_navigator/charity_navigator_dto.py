from enum import Enum
from dataclasses import dataclass

app_id = '998e64be'
app_key = 'c99ca3e66a3f61b839486371709a0cd4'


class SearchType(Enum):
    DEFAULT = ''
    NAME_ONLY = 'Organization Name'


class ScopeType(Enum):
    ALL = ''
    REGIONAL = 'Regional'
    NATIONAL = 'National'
    INTERNATIONAL = 'International'


class SortType(Enum):
    RELEVANCE = 'Relevance'
    RATING = 'Rating'
    NAME = 'Name'


class StateType(Enum):
    DEFAULT = ''
    AL = 'Alabama'
    AK = 'Alaska'
    AZ = 'Arizona'
    AR = 'Arkansas'
    CA = 'California'
    CO = 'Colorado'
    CT = 'Connecticut'
    DE = 'Delaware'
    FL = 'Florida'
    GA = 'Georgia'
    HI = 'Hawaii'
    ID = 'Idaho'
    IL = 'Illinois'
    IN = 'Indiana'
    IA = 'Iowa'
    KS = 'Kansas'
    KY = 'Kentucky'
    LA = 'Louisiana'
    ME = 'Maine'
    MD = 'Maryland'
    MA = 'Massachusetts'
    MI = 'Michigan'
    MN = 'Minnesota'
    MS = 'Mississippi'
    MO = 'Missouri'
    MT = 'Montana'
    NE = 'Nebraska'
    NV = 'Nevada'
    NH = 'New Hampshire'
    NJ = 'New Jersey'
    NM = 'New Mexico'
    NY = 'New York'
    NC = 'North Carolina'
    ND = 'North Dakota'
    OH = 'Ohio'
    OK = 'Oklahoma'
    OR = 'Oregon'
    PA = 'Pennsylvania'
    RI = 'Rhode Island'
    SC = 'South Carolina'
    SD = 'South Dakota'
    TN = 'Tennessee'
    TX = 'Texas'
    UT = 'Utah'
    VT = 'Vermont'
    VA = 'Virginia'
    WA = 'Washington'
    WV = 'West Virginia'
    WI = 'Wisconsin'
    WY = 'Wyoming'


filter_values = {'searchType': list(SearchType), 'scopeType': list(ScopeType), 'sortType': list(SortType),
                 'stateType': list(StateType)}


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
