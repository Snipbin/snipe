from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.account.models import SnipeUser
from apps.snippet.models import PrivacyChoices


class ProfileView(LoginRequiredMixin, View):
    profile_page = 'account/profile_page.html'

    def get(self, request, username):
        context = dict()
        user: SnipeUser = SnipeUser.objects.all().filter(username=username).first()
        if user is None:
            return render(request, '404.html', context)
        snippets = user.snipes.all().order_by('-last_modified')
        if request.user.username != user.username:
            snippets = snippets.filter(is_private=PrivacyChoices.PUBLIC)
        context['snippets'] = snippets
        return render(request, self.profile_page, context)
