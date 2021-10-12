from django.shortcuts import render, redirect
from django.views import View
from application.api.charity_navigator import get_organizations


class Search(View):
    def get(self, request):
        charities = get_organizations({'search': request.GET['q']})
        return render(request, "main/search.html", {'search': request.GET['q'], 'charities': charities})

    def post(self, request):
        return redirect("/search?q=" + request.POST['search'])
