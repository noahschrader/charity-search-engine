import datetime
import typing

from django.shortcuts import render
from django.views import View

from application.api.charity_navigator import get_organizations, SortType
from application.fema.FEMA import DisasterQuery, DateFilter, Filter, ApiHandler, DeclarationTypeFilter


def get_disaster_title_list(disasters: typing.Dict):
    lst = []
    for d in disasters:
        lst.append(d[DisasterQuery.Field.DECLARATION_TITLE.value])
    return lst


def count_strings(lst: typing.List[str]) -> typing.Dict:
    counts = {}
    for s in lst:
        if s not in counts.keys():
            counts[s] = 0
        counts[s] += 1
    return counts


def lookup_recent_disasters():
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
    title_counts = count_strings(titles)
    sorted_counts = dict(sorted(title_counts.items(), key=lambda item: item[1], reverse=True))
    return list(sorted_counts.keys())


class Home(View):
    def get(self, request):
        top_disasters = lookup_recent_disasters()

        return render(request, "main/home.html", {"disasters": top_disasters})
