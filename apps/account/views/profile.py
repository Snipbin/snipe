from django.shortcuts import render
from django.views import View

from apps.account.models import SnipeUser


class ProfileView(View):
    profile_page = 'account/profile_page.html'

    def get(self, request, username):
        context = dict()
        user = SnipeUser.objects.all().filter(username=username).first()
        if user is None:
            return render(request, '404.html', context)
        context['snippets'] = user.snipes.all().order_by('last_modified').reverse()
        return render(request, self.profile_page, context)

    def post(self):
        pass
