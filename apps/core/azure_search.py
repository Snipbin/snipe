import requests
from django.conf import settings
from requests import Response

base_url = 'https://{service_name}.search.windows.net/indexes/{index_name}/docs'

post_url = f'{base_url}/index'


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
