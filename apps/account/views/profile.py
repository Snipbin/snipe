from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View

from apps.account.models import UserProfile


class ProfileView(View):
    profile_page = 'account/profile_page.html'

    def get(self, request, username):
        context = dict()
        user = User.objects.all().filter(username=username).first()
        user_profile = UserProfile.objects.all().filter(user=user).first()
        if user_profile is None:
            return render(request, '404.html', context)
        context['user_profile'] = user_profile
        context['snippets'] = user_profile.snipes.all().order_by('last_modified').reverse()
        return render(request, self.profile_page, context)

    def post(self):
        pass
