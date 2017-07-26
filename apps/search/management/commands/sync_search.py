from django.conf import settings
from django.core.management import BaseCommand
from requests import HTTPError

from apps.search.azure_search import AzureSearch
from apps.search.models import SearchUpdate
from apps.search.serializers import SearchUpdateSerializer
from apps.snippet.models import SnippetSearchUpdate, Snippet


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--all', dest='all', default=False, action='store_true',
                            help='Add all entries')
        parser.add_argument('--delete', dest='delete', default=False, action='store_true',
                            help='Delete all entries from search index')

    def handle(self, **options):
        is_all = options['all']

        search_updates = []
        snippets_updates = None

        if not is_all:
            snippets_updates = SnippetSearchUpdate.objects.filter(
                pushed=False).select_related('snippet','snippet__author', 'snippet__language')

            for snippet_update in snippets_updates:
                if snippet_update.deletable_id is None:
                    search_update = SearchUpdate(
                        snippet_update.snippet.uid,
                        snippet_update.snippet.title,
                        snippet_update.snippet.description,
                        snippet_update.snippet.code,
                        snippet_update.snippet.author.username.lower(),
                        snippet_update.snippet.language.name.lower(),
                    )
                else:
                    search_update = SearchUpdate(
                        id_=snippet_update.deletable_id,
                        action="delete",
                    )

                search_updates.append(search_update)

        else:
            snippets = Snippet.objects.all().select_related('author', 'language')

            for snippet in snippets:
                search_update = SearchUpdate(
                    snippet.uid,
                    snippet.title,
                    snippet.description,
                    snippet.code,
                    snippet.author.username.lower(),
                    snippet.language.name.lower(),
                )
                search_updates.append(search_update)

        if not search_updates:
            self.stdout.write("No updates to run!")
            return

        serialized_data = SearchUpdateSerializer(search_updates, many=True).data

        azure_search_post_data = {
            "value": serialized_data,
        }

        snippet_search = AzureSearch(settings.AZURE_SEARCH_OPTIONS['snippet_index'])
        response = snippet_search.post_data(azure_search_post_data)
        request_body = response.request.body

        self.stdout.write(f"Request Data: {request_body}")
        self.stdout.write(f"Response status code: {response.status_code}")
        self.stdout.write(f"Response body: {response.json()}")

        try:
            response.raise_for_status()
            if snippets_updates:
                snippets_updates.update(pushed=True)
        except HTTPError:
            pass
