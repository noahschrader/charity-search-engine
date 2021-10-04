from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
from charity.models import *
import datetime

class Home(View):
    def get(self, request):
        #  For the get method of home, clear the current user as the first line of code. So going to the home page (via get) is equivalent to logging out.
        request.session.pop("username", None)
        return render(request, "main/home.html")