from uuid import UUID

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import View

from apps.snippet.models import Snippet, SnippetViews


class SnippetView(LoginRequiredMixin, View):
    snippet_page = 'snippet/view.html'

    def get(self, request, uid):
        context = dict()
        if self.is_valid_uuid(uid):

            snippet: Snippet = Snippet.objects.all().filter(
                uid=uid,
            ).prefetch_related('language', 'author').annotate(
                bookmarks_count=Count('bookmarks', distinct=True),
                views_count=Count('views', distinct=True),
            ).first()
            if snippet is not None:
                view, created = SnippetViews.objects.get_or_create(snippet=snippet, user=request.user)
                if created:
                    snippet.views_count += 1

                if snippet.is_author_private() and snippet.author_id != request.user.id:
                    return HttpResponseForbidden()
                context['snippet'] = snippet
                return render(request, self.snippet_page, context)
            else:
                raise Http404()
        else:
            raise Http404()

    @staticmethod
    def is_valid_uuid(uuid_to_test, version=4):
        try:
            uuid_obj = UUID(uuid_to_test, version=version)
        except ValueError:
            return False

        return str(uuid_obj).replace('-', '') == uuid_to_test
