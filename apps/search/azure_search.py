from typing import List

import logging
import requests
from django.conf import settings
from requests import Response, HTTPError

from apps.core.utils import VIEW_PAGE_SIZE
from apps.search.models import AzureSearchResponse
from apps.search.serializers import AzureSearchResponseSerializer

base_url = 'https://{service_name}.search.windows.net/indexes/{index_name}/docs'

post_url = f'{base_url}/index'

logger = logging.getLogger(__name__)


class AzureSearch(object):

    def __init__(self, index_name, service_name=None, api_key=None, api_version=None):
        self.service_name = service_name if service_name else settings.AZURE_SEARCH_OPTIONS['service-name']
        self.index_name = index_name
        self.api_key = api_key if api_key else settings.AZURE_SEARCH_OPTIONS['api-key']
        self.api_version = api_version if api_version else settings.AZURE_SEARCH_OPTIONS['api-version']
        self.session = self.init_session()

    @property
    def post_url(self):
        return post_url.format(service_name=self.service_name, index_name=self.index_name)

    @property
    def query_url(self):
        return base_url.format(service_name=self.service_name, index_name=self.index_name)

    def init_session(self):
        session = requests.Session()
        session.headers.update(
            {
                'api-key': self.api_key,
            },
        )
        session.params.update(
            {
                'api-version': self.api_version,
            },
        )
        return session

    def post_data(self, data) -> Response:
        result = self.session.post(
            self.post_url,
            json=data,
        )
        return result

    def query_data(self, query: dict) -> Response:
        result = self.session.get(
            self.query_url,
            params=query
        )
        return result


class AzureSnippetSearch(AzureSearch):

    def __init__(self, index_name=None, service_name=None, api_key=None, api_version=None,
                 search=None, authors: List[str]=None, languages: List[str]=None, skip=0, top=VIEW_PAGE_SIZE,
                 ):
        if not index_name:
            index_name = settings.AZURE_SEARCH_OPTIONS['snippet_index']
        super().__init__(index_name, service_name, api_key, api_version)
        self.search = search
        self.authors = authors
        self.languages = languages
        self.skip = skip
        self.top = top
        self.result: AzureSearchResponse = None

    @property
    def query_dict(self) -> dict:
        query_dict = {
            "$top": self.top,
            "$count": "true",
        }
        if self.search:
            query_dict['search'] = self.search

        if self.skip and self.skip > 0:
            query_dict['$skip'] = self.skip

        filter_queries = []
        if self.authors:
            author_queries = []
            for author in self.authors:
                author_queries.append(f"author eq '{author.lower()}'")
            odata_expression = ' or '.join(author_queries)
            if odata_expression:
                filter_queries.append(f'({odata_expression})')
        if self.languages:
            language_queries = []
            for language in self.languages:
                language_queries.append(f"language eq '{language.lower()}'")
            odata_expression = ' or '.join(language_queries)
            if odata_expression:
                filter_queries.append(f'({odata_expression})')

        if filter_queries:
            query_dict["$filter"] = " and ".join(filter_queries)

        return query_dict

    @property
    def next_skip(self) -> int:
        count = self.result.count
        if self.skip + self.top >= count:
            return -1
        return self.skip + self.top

    def has_next(self) -> bool:
        return self.skip + self.top < self.result.count

    def has_previous(self) -> bool:
        return self.skip > 0

    @property
    def previous_skip(self) -> int:
        dummy_prev = self.skip - self.top
        if dummy_prev > 0:
            return dummy_prev
        return 0

    def query_snippet_data(self) -> AzureSearchResponse:
        result = super().query_data(self.query_dict)

        try:
            result.raise_for_status()
        except HTTPError:
            logging.exception(f"Received status code: {result.status_code}")
            logging.debug(result.json())
            raise

        data = result.json()

        serializer = AzureSearchResponseSerializer(data=data)
        if serializer.is_valid():
            self.result = serializer.save()
            return self.result
        else:
            logging.error(serializer.errors)
            raise HTTPError()
