from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.snippet.models import Snippet, PrivacyChoices


class DiscoverView(LoginRequiredMixin, View):
    discover_page = 'snippet/discover.html'

    def get(self, request):
        context = dict()
        public_snippets = Snippet.objects.filter(is_private=PrivacyChoices.PUBLIC).order_by('-last_modified')
        my_snippets = Snippet.objects.filter(author_id=request.user.id).order_by('-last_modified')
        snippets = public_snippets | my_snippets
        context['snippets'] = snippets
        return render(request, self.discover_page, context)
