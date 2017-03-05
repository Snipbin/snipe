from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.account.models import SnipeUser


class ProfileView(LoginRequiredMixin, View):
    profile_page = 'account/profile_page.html'
    login_url = '/auth/login/'
    redirect_field_name = 'redirect'

    def get(self, request, username):
        context = dict()
        user = SnipeUser.objects.all().filter(username=username).first()
        if user is None:
            return render(request, '404.html', context)
        context['snippets'] = user.snipes.all().filter(is_private='PUBLIC').order_by('last_modified').reverse()
        return render(request, self.profile_page, context)

    def post(self):
        pass
