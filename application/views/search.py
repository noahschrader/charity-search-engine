from django.shortcuts import render
from django.views import View
from application.api.charity_navigator.charity_navigator import get_organizations
from application.api.charity_navigator.charity_navigator_dto import CharityNavigatorDto, SearchType, ScopeType, \
    SortType, StateType, filter_values


class SearchView(View):
    def __init__(self):
        super().__init__()
        self.applied_filters = {}

    def store_applied_filters(self, request):
        self.applied_filters = {'city': request.GET.get('city', ''),
                                'scope': request.GET.get('scope', ''),
                                'searchType': request.GET.get('searchType', ''),
                                'sort': request.GET.get('sort', 'Relevance'),
                                'state': request.GET.get('state', ''),
                                'zip': request.GET.get('zip', '')}

    def construct_dto(self, request):
        return CharityNavigatorDto(city=self.applied_filters['city'],
                                   pageNum=int(request.GET.get('pageNum', 1)),
                                   scope=ScopeType(self.applied_filters['scope']).name,
                                   search=request.GET.get('q', ''),
                                   searchType=SearchType(self.applied_filters['searchType']).name,
                                   sort=SortType(self.applied_filters['sort']).name,
                                   state=StateType(self.applied_filters['state']).name,
                                   zip=self.applied_filters['zip'])

    def get(self, request):
        self.store_applied_filters(request)
        dto = self.construct_dto(request)
        charities = get_organizations(dto)
        dto.pageNum = dto.pageNum + 1
        has_next = len(get_organizations(dto)) > 0
        return render(request, 'main/search.html',
                      {'search': dto.search, 'charities': charities, 'pageNum': dto.pageNum - 1, 'hasNext': has_next,
                       'filter_values': filter_values, 'applied_filters': self.applied_filters})
