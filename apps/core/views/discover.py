from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.snippet.models import Snippet


class DiscoverView(LoginRequiredMixin, View):
    discover_page = 'snippet/discover.html'
    login_url = '/auth/login/'
    redirect_field_name = 'redirect'

    def get(self, request):
        context = dict()
        snippets = Snippet.objects.all().filter(is_private='PUBLIC').order_by('last_modified').reverse()
        context['snippets'] = snippets
        return render(request, self.discover_page, context)

    def post(self, request):
        pass
