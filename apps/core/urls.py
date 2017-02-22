from django.conf.urls import url

from apps.core.views.new_snippet import NewSnippet

urlpatterns = [
    url(r'^$', NewSnippet.as_view(), name='home'),
]
