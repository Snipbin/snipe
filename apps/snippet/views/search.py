import re
from django.views import View


author_regex = r'author:[^\s]+'
language_regex = r''


def parse_search_query(query):



class Search(View):
    def get(self, request):
        page = request.PAGE.get('page')

        try:
            page = int(page)
        except (ValueError, TypeError):
            page = 1

