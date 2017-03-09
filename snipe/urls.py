"""Snipe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from apps.snippet import urls as snippet_urls
from apps.account import urls as account_urls
from apps.authentication import urls as auth_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include(auth_urls, namespace='authentication')),
    url(r'^home/', include('apps.core.urls', namespace='core')),
    url(r'^', include(snippet_urls, namespace='snippet')),
    url(r'^(?P<username>[\w{}.-]+)/', include(account_urls, namespace='account')),
]
