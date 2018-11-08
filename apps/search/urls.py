from django.conf.urls import url

from apps.search.views import SnippetSearchView

app_name = 'apps.search'
urlpatterns = [
    url(r'^$', SnippetSearchView.as_view(), name='search'),
]
