from django.conf.urls import url

from apps.core.views.home import Home

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
]
