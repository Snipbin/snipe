from django.conf.urls import url

from apps.core.views.discover import DiscoverView
from apps.core.views.new_snippet import NewSnippetView

urlpatterns = [
    url(r'^$', NewSnippetView.as_view(), name='new_snippet'),
    url(r'^discover/$', DiscoverView.as_view(), name='discover')
]
