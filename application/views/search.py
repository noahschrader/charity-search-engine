from django.shortcuts import render
from django.views import View
from application.api.charity_navigator import get_organizations


class Search(View):
    def get(self, request):
        return render(request, "main/search.html")

    def post(self, request):
        charities = get_organizations({'search': request.POST['search']})
        return render(request, "main/search.html", {'search': request.POST['search'], 'charities': charities})
