from django.conf.urls import url

from apps.snippet.views.snippet import SnippetView

urlpatterns = [
    url(r'^$', SnippetView.as_view(), name='snippet'),
]
