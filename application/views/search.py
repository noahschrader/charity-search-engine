from django.shortcuts import render
from django.views import View
from application.api.charity_navigator import get_organizations


class Search(View):
    def get(self, request):
        search_term = request.GET.get('q', '')
        page_num = int(request.GET.get('pageNum', 1))
        charities = get_organizations({'search': search_term, 'pageNum': page_num})
        has_next = len(get_organizations({'search': search_term, 'pageNum': page_num + 1})) > 0
        return render(request, "main/search.html",
                      {'search': search_term, 'charities': charities, 'pageNum': page_num, 'hasNext': has_next})
