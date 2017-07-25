from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render

from apps.account.models import SnipeUser
from apps.core.views.pagination import PaginationView
from apps.snippet.models import PrivacyChoices


class ProfileView(LoginRequiredMixin, PaginationView):
    profile_page = 'account/profile_page.html'

    def get(self, request, username):
        user: SnipeUser = SnipeUser.objects.all().filter(username=username).first()

        if user is None:
            return render(request, '404.html')

        snippets = user.snipes.all().order_by('-last_modified').annotate(
            bookmarks_count=Count('bookmarks', distinct=True),
            views_count=Count('views', distinct=True),
        )

        if request.user.username != user.username:
            snippets = snippets.filter(is_private=PrivacyChoices.PUBLIC)

        snippets = self.get_page(snippets)

        context = {
            'snippets': snippets,
        }

        context = self.update_pagination_context(context)

        return render(request, self.profile_page, context)
