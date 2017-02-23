from django.conf.urls import url

from apps.core.views.new_snippet import NewSnippetView

urlpatterns = [
    url(r'^$', NewSnippetView.as_view(), name='new_snippet'),
]
