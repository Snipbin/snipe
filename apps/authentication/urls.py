from django.conf.urls import url

from apps.authentication.views import AdalLoginView, AdalRedirectHandlerView, LogoutView

app_name = 'app.authentication'
urlpatterns = [
    url(r'^login/$', AdalLoginView.as_view(), name='login'),
    url(r'^login/redirect/$', AdalRedirectHandlerView.as_view(), name='adal_redirect'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
]
