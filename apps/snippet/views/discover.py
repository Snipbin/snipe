from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import render
from django.views import View

from apps.snippet.models import Snippet, PrivacyChoices


class DiscoverView(LoginRequiredMixin, View):
    discover_page = 'snippet/discover.html'

    def get(self, request):
        context = dict()
        snippets = Snippet.objects.filter(
            Q(is_private=PrivacyChoices.PUBLIC) | Q(author_id=request.user.id)
        ).order_by('-last_modified').annotate(
            bookmarks_count=Count('bookmarks'),
        )
        context['snippets'] = snippets
        return render(request, self.discover_page, context)
