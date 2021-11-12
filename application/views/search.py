from django.shortcuts import render
from django.views import View
from application.api.charity_navigator.charity_navigator import get_organizations
from application.api.charity_navigator.charity_navigator_dto import CharityNavigatorDto, filters


class Search(View):
    def construct_dto(self, request):
        return CharityNavigatorDto(search=request.GET.get('q', ''), pageNum=int(request.GET.get('pageNum', 1)),
                                   city=request.GET.get('city', ''), state=request.GET.get('state', ''),
                                   zip=request.GET.get('zip', ''), sort=request.GET.get('sort', ''),
                                   scope=request.GET.get('scope', ''), searchType=request.GET.get('searchType', ''))

    def get(self, request):
        dto = self.construct_dto(request)
        charities = get_organizations(dto)
        dto.pageNum = dto.pageNum + 1
        has_next = len(get_organizations(dto)) > 0
        return render(request, "main/search.html",
                      {'search': dto.search, 'charities': charities, 'pageNum': dto.pageNum - 1, 'hasNext': has_next,
                       'filters': filters})
