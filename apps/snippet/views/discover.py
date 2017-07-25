from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import render

from apps.core.views.pagination import PaginationView
from apps.snippet.models import Snippet, PrivacyChoices


class DiscoverView(LoginRequiredMixin, PaginationView):
    discover_page = 'snippet/discover.html'

    def get(self, request):

        page = request.GET.get(self.page_name)

        snippets = Snippet.objects.filter(
            Q(is_private=PrivacyChoices.PUBLIC) | Q(author_id=request.user.id)
        ).order_by('-last_modified').annotate(
            bookmarks_count=Count('bookmarks', distinct=True),
            views_count=Count('views', distinct=True),
        )

        snippets = self.get_page(snippets)

        context = {
            'snippets': snippets,
        }

        context = self.update_pagination_context(context)

        return render(request, self.discover_page, context)
