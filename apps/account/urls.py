from django.conf.urls import url

from apps.account.views.profile import Profile

urlpatterns = [
    url(r'^$', Profile.as_view(), name='profile'),
]
