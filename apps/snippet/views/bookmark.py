from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views import View

from apps.snippet.models import Snippet, Bookmark


class BookmarkView(LoginRequiredMixin, View):
    """
    Add or Delete bookmark. If bookmark is already present then delete it else add it
    """

    def post(self, request, uid):
        snippet: Snippet = Snippet.objects.filter(uid=uid).first()
        if not snippet:
            raise Http404()

        snippet_data = {
            'snippet': snippet,
            'user': request.user,
        }
        bookmark = Bookmark.objects.filter(**snippet_data).first()
        if not bookmark:
            bookmark = Bookmark(
                **snippet_data,
            )
            bookmark.save()
        else:
            bookmark.delete()

        return redirect('snippet:snippet', uid=uid)
