import datetime
import typing

from django.shortcuts import render
from django.views import View

from application.api.charity_navigator import get_organizations
from application.fema.FEMA import DisasterQuery, DateFilter, Filter, ApiHandler


def get_disaster_title_list(disasters: typing.Dict):
    lst = []
    for d in disasters:
        lst.append(d[DisasterQuery.Field.DECLARATION_TITLE.value])
    return lst

def get_kth_most_occurring(lst: typing.List[str]) -> str:
    counts = {}
    for s in lst:
        if s not in counts.keys():
            counts[s] = 0
        counts[s] += 1
    print(str(counts))
    common_title = ""
    max_count = 0
    for t, c in counts.items():
        if c > max_count:
            common_title = t
            max_count = c
    return common_title


def lookup_recent_disaster_charities():
    query = DisasterQuery()

    # Setup date filter for records from the last 30 days.
    thirty_day_time_delta = datetime.timedelta(days=90)
    start_date = datetime.datetime.today() - thirty_day_time_delta
    date_filter = DateFilter(Filter.LogicalOperator.GREATER_THAN, start_date)

    query.add_filter(date_filter)
    handler = ApiHandler()

    # Query for disasters.
    disasters = handler.query(query)

    titles = get_disaster_title_list(disasters)
    print(str(titles))
    most_common_disaster_title = get_kth_most_occurring(titles)
    print("most common title: " + most_common_disaster_title)
    charities = get_organizations({'search': most_common_disaster_title, 'pageNum': 1})
    print(charities)


class Home(View):
    def get(self, request):
        return render(request, "main/home.html")
