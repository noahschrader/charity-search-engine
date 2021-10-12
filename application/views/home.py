from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from application.api.charity_navigator import get_organizations


class Home(View):
    def get(self, request):
        return render(request, "main/home.html")

    def post(self, request):
        return redirect("/search?q=" + request.POST['search'])
