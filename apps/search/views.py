import json
import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from apps.search.azure_search import AzureSnippetSearch
from apps.snippet.models import PrivacyChoices, Snippet


class SnippetSearchView(LoginRequiredMixin, View):
    regex = re.compile(r'^([^:]+):([^\s]+)\s*', re.IGNORECASE)

    @staticmethod
    def process_match(matches):
        authors = []
        languages = []

        for match in matches:
            groups = match.groups()
            key = groups[0].lower()
            value = groups[1].lower()
            values = value.split(',')
            if key == "author":
                authors.extend(values)
            elif key == "lang":
                languages.extend(values)
            else:
                # Ignoring other kind of filters for now
                pass

        return authors, languages

    def parse_search_query(self, query: str):
        query = query.strip()
        matches = []
        while True:
            match = self.regex.match(query)
            if match:
                matches.append(match)
                query = self.regex.sub('', query, count=1)
            else:
                break

        query = query.strip("'\"")
        authors, languages = self.process_match(matches)

        search = AzureSnippetSearch(authors=authors, languages=languages, search=query)
        return search

    def get(self, request):
        query = request.GET.get('query')
        skip = request.GET.get('skip')
        try:
            skip = int(skip)
            if skip < 0:
                skip = 0
        except (TypeError, ValueError):
            skip = 0

        if not query:
            return render(request, 'snippet/search.html', {})

        search = self.parse_search_query(query)
        search.skip = skip

        result = search.query_snippet_data()

        scores = {}

        for val in result.value:
            uid = val['id_']
            score = val['score']

            scores[uid] = score

        snippets = Snippet.objects.filter(uid__in=list(scores.keys())).filter(
            Q(is_private=PrivacyChoices.PUBLIC) | Q(author_id=request.user.id)
        ).annotate(
            bookmarks_count=Count('bookmarks', distinct=True),
            views_count=Count('views', distinct=True),
        )

        snippets = sorted(snippets, key=lambda snippet: scores.get(str(snippet.uid)), reverse=True)

        base_url = reverse('search:search')
        next_url = f'{base_url}?query={query}&skip={search.next_skip}'
        previous_url = f'{base_url}?query={query}&skip={search.previous_skip}'

        context = {
            'snippets': snippets,
            'count': result.count,
            'next_disabled': '' if search.has_next() else 'disabled',
            'previous_disabled': '' if search.has_previous() else 'disabled',
            'next_url': next_url,
            'previous_url': previous_url,
        }

        return render(request, 'snippet/search.html', context)

