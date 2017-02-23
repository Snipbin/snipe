from django.conf.urls import url

from apps.account.views.profile import ProfileView

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='user'),
]
