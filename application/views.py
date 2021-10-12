from django.shortcuts import render
from django.views import View
from api.charity_navigator import get_organizations
import json

# Create your views here.

class NameSearch(View):
    def get(self, request, query):
        #  For the get method of NameSearch, receive the query, submit it to the API, and return the results
        r = get_organizations({"search": query, "rated": "TRUE"})   # Send the query to the get_organizations method to obtain results from the API

        return render(request, "main/home.html")
