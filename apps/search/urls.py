from django.conf.urls import url

from apps.search.views import SnippetSearchView

urlpatterns = [
    url(r'^$', SnippetSearchView.as_view(), name='search'),
]
