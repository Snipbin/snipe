from django.conf.urls import url

from apps.snippet.views.bookmark import BookmarkView
from apps.snippet.views.discover import DiscoverView
from apps.snippet.views.new import NewSnippetView
from apps.snippet.views.snippet import SnippetView
from apps.snippet.views.snippet_delete import SnippetDeleteView
from apps.snippet.views.snippet_edit import SnippetEditView

urlpatterns = [
    url(r'^$', NewSnippetView.as_view(), name='new'),
    url(r'^discover/$', DiscoverView.as_view(), name='discover'),
    url(r'^(?P<uid>\w+)/$', SnippetView.as_view(), name='snippet'),
    url(r'^(?P<uid>\w+)/bookmark/$', BookmarkView.as_view(), name='bookmark'),
    url(r'^(?P<uid>\w+)/delete/$', SnippetDeleteView.as_view(), name='snippet_delete'),
    url(r'^(?P<uid>\w+)/edit/$', SnippetEditView.as_view(), name='snippet_edit'),
]
