from django.conf.urls import url

from apps.account.views.profile import ProfileView

app_name = 'apps.account'
urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='user'),
]
