from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import render

from apps.core.views.pagination import PaginationView
from apps.snippet.models import Snippet, PrivacyChoices


class DiscoverView(LoginRequiredMixin, PaginationView):
    discover_page = 'snippet/discover.html'

    def get(self, request):

        sort_option = request.GET.get('s')
        if sort_option not in ['c', 'm']:
            sort_option = 'm'           # Default sort by modified

        direction_option = request.GET.get('d')
        if direction_option not in ['d', 'a']:
            direction_option = 'd'      # Default is descending

        order_by = 'last_modified'
        if sort_option == 'c':
            order_by = 'created_at'

        if direction_option == 'd':
            order_by = f'-{order_by}'

        snippets = Snippet.objects.filter(
            Q(is_private=PrivacyChoices.PUBLIC) | Q(author_id=request.user.id)
        ).order_by(order_by).annotate(
            bookmarks_count=Count('bookmarks', distinct=True),
            views_count=Count('views', distinct=True),
        )

        snippets = self.get_page(snippets)

        context = {
            'snippets': snippets,
            'order_by': f'{sort_option}{direction_option}'
        }

        context = self.update_pagination_context(context)

        return render(request, self.discover_page, context)
