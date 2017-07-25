from django.conf import settings
from django.core.management import BaseCommand
from requests import HTTPError
import json

from apps.core.azure_search import AzureSearch
from apps.snippet.models import SnippetSearchUpdate, Snippet
from rest_framework import serializers


class SearchUpdate(object):

    def __init__(self, id_, title=None, description=None, code=None, author=None, language=None, action="upload"):
        self.action = action
        self.id_ = id_
        self.title = title
        self.description = description
        self.code = code
        self.author = author
        self.language = language


class SearchUpdateSerializer(serializers.Serializer):

    action = serializers.ChoiceField(choices=["upload", "delete"], default="upload")
    id_ = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    code = serializers.CharField()
    author = serializers.CharField()
    language = serializers.CharField()

    def to_representation(self, instance):
        initial = super().to_representation(instance)
        initial["@value.action"] = initial["action"]
        initial["id"] = initial["id_"]
        del initial["action"]
        del initial["id_"]
        return initial


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--all', dest='all', default=False, action='store_true',
                            help='Add all entries')
        parser.add_argument('--delete', dest='delete', default=False, action='store_true',
                            help='Delete all entries from search index')

    def handle(self, **options):
        is_all = options['all']
        delete = options['delete']

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
                        snippet_update.snippet.author.username,
                        snippet_update.snippet.language.name,
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
                    snippet.author.username,
                    snippet.language.name,
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
