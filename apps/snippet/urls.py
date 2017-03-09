from django.conf.urls import url

from apps.snippet.views.discover import DiscoverView
from apps.snippet.views.new import NewSnippetView
from apps.snippet.views.snippet import SnippetView

urlpatterns = [
    url(r'^$', NewSnippetView.as_view(), name='new'),
    url(r'^discover/$', DiscoverView.as_view(), name='discover'),
    url(r'^(?P<username>[\w{}.-]+)/(?P<uid>[\w{}.-]+)/$', SnippetView.as_view(), name='snippet'),
]
