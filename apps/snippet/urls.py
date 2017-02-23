from django.conf.urls import url

from apps.snippet.views.snippet import Snippet

urlpatterns = [
    url(r'$', Snippet.as_view(), name='snippet'),
]
