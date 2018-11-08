from django.conf.urls import url

from apps.core.views.home import HomeView

app_name = 'apps.core'
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
]
