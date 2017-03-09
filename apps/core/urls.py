from django.conf.urls import url

from apps.core.views.home import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
]
