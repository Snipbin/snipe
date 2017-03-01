from django.conf.urls import url

from apps.authentication.views import AdalLoginView, AdalRedirectHandlerView

urlpatterns = [
    url(r'^login/$', AdalLoginView.as_view(), name='login'),
    url(r'^login/redirect/$', AdalRedirectHandlerView.as_view(), name='adal_redirect'),
]
