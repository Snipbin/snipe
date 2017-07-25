import adal
import requests
from adal import AdalError
from django.conf import settings
from django.contrib.auth import login, logout
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from apps.account.models import SnipeUser


def get_adal_authority() -> str:
    tenant_id = settings.ADAL_TENANT_ID
    return "https://login.microsoftonline.com/{}".format(tenant_id)


def get_redirect_uri(request: HttpRequest) -> str:
    return request.build_absolute_uri(reverse('authentication:adal_redirect'))


class AdalLoginView(View):
    def get(self, request):
        return redirect(self._build_auth_url())

    def _build_auth_url(self) -> str:
        tenant_id = settings.ADAL_TENANT_ID
        client_id = settings.ADAL_APP_ID
        redirect_uri = get_redirect_uri(self.request)
        adal_auth_url = ("https://login.microsoftonline.com/{}/oauth2/authorize?"
                         "response_type=code&"
                         "client_id={}&"
                         "redirect_uri={}&"
                         ).format(tenant_id, client_id, redirect_uri)
        return adal_auth_url


class AdalRedirectHandlerView(View):
    def get(self, request: HttpRequest):
        code = request.GET.get("code")
        if code is None:
            return redirect('/')
        context = adal.AuthenticationContext(get_adal_authority())

        try:

            token = context.acquire_token_with_authorization_code(
                code,
                get_redirect_uri(request),
                "https://graph.windows.net",
                settings.ADAL_APP_ID,
                settings.ADAL_APP_SECRET,
            )
        except AdalError as ex:
            raise PermissionDenied(ex)

        access_token = token['accessToken']

        # Get graph data
        data = requests.get("https://graph.windows.net/me",
                            params={
                                "api-version": "1.6",
                            },
                            headers={
                                "Authorization": "Bearer {0}".format(access_token),
                            })
        me = data.json()

        user_oid = me["objectId"]
        tenant_id = token["tenantId"]
        refresh_token = token['refreshToken']
        email = me['mail']
        if not email:
            email = me['otherMails'][0] if len(me['otherMails']) else ''
        alias = me['mailNickname'] if me['mailNickname'] else me['userPrincipalName']

        user, _ = SnipeUser.objects.update_or_create(
            object_id=user_oid, tenant_id=tenant_id,
            defaults={
                'username': alias,
                'refresh_token': refresh_token,
                'email': email,
                'first_name': me['givenName'],
                'last_name': me['surname'],
                'job_title': me['jobTitle'],
                'department': me['department'],
            })

        login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])

        return redirect('account:user', username=user.username)


class LogoutView(View):

    def post(self, request):
        logout(request)
        return redirect('/home')
