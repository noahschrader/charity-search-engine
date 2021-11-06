import datetime
import typing
from typing import List, Dict

from django.shortcuts import render
from django.views import View

from application.fema.FEMA import DisasterQuery, DateFilter, Filter, ApiHandler


def get_list_of_disaster_titles(disasters: typing.Dict):
    lst = []
    for d in disasters:
        lst.append(d[DisasterQuery.Field.DECLARATION_TITLE.value])
    return lst


def count_strings_in_list(lst: List[str]) -> Dict:
    counts = {}
    for s in lst:
        if s not in counts.keys():
            counts[s] = 0
        counts[s] += 1
    return counts


def lookup_recent_disasters(scope_in_days=90) -> List[str]:
    """
    Queries the FEMA API for disasters that were declared a timeframe before today.
    :param scope_in_days: The number of days in the past to consider for disasters.
    :return: A list of disaster titles sorted from most declared to least declared.
    """
    query = DisasterQuery()

    # Setup date filter for records from the last 30 days.
    thirty_day_time_delta = datetime.timedelta(days=scope_in_days)
    start_date = datetime.datetime.today() - thirty_day_time_delta
    date_filter = DateFilter(Filter.LogicalOperator.GREATER_THAN, start_date)

    query.add_filter(date_filter)
    handler = ApiHandler()

    # Query for disasters.
    disasters = handler.query(query)

    titles = get_list_of_disaster_titles(disasters)
    title_counts = count_strings_in_list(titles)
    sorted_counts = dict(sorted(title_counts.items(), key=lambda item: item[1], reverse=True))
    return list(sorted_counts.keys())


class Button:

    def __init__(self, text="", is_selected=False):
        """
        :param text: The text to be displayed on the button.
        :param is_selected: Indicates if a button is currently selected.
        """
        self.text = text
        self.is_selected = is_selected

    def get_text(self) -> str:
        """
        :return: The current text value of this button.
        """
        return self.text

    def set_text(self, new_text) -> str:
        """
        Sets the text of the button.
        :param new_text: Text to be set to.
        :return: The old text.
        """
        prev = self.text
        self.text = new_text
        return prev


class Home(View):

    def get(self, request):
        menu_buttons = [
            vars(Button("Recent Disasters", True)),
            vars(Button("Nearby Charities", False))
        ]
        print(menu_buttons)
        top_disasters = lookup_recent_disasters()[0:10]
        return render(request, "main/home.html", {"items": top_disasters, "menu_options": menu_buttons})
