from django.shortcuts import render
from django.views import View
from application.api.charity_navigator.charity_navigator import get_organizations
from application.api.charity_navigator.charity_navigator_dto import CharityNavigatorDto, SearchType, ScopeType, SortType, StateType, filters


class Search(View):
    def construct_dto(self, request):
        state = StateType(request.GET.get('state', '')).name
        sort = SortType(request.GET.get('sort', 'Relevance')).name
        scope = ScopeType(request.GET.get('scope', '')).name
        searchType = SearchType(request.GET.get('searchType', '')).name
        return CharityNavigatorDto(search=request.GET.get('q', ''), pageNum=int(request.GET.get('pageNum', 1)),
                                   city=request.GET.get('city', ''), state=state, zip=request.GET.get('zip', ''),
                                   sort=sort, scope=scope, searchType=searchType)

    def get(self, request):
        dto = self.construct_dto(request)
        charities = get_organizations(dto)
        dto.pageNum = dto.pageNum + 1
        has_next = len(get_organizations(dto)) > 0
        return render(request, 'main/search.html',
                      {'search': dto.search, 'charities': charities, 'pageNum': dto.pageNum - 1, 'hasNext': has_next,
                       'filters': filters})
