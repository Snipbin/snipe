from django.shortcuts import render
from django.views.generic import View

from apps.snippet.models import Snippet


class SnippetView(View):

    def get(self, request, username, uid):
        context = dict()
        snippet = Snippet.objects.all().filter(uid=uid, author__user__username=username)\
            .prefetch_related('language', 'author').first()
        if snippet is not None:
            context['snippet'] = snippet
            return render(request, 'snippet/snippet.html', context)
        else:
            return render(request, '404.html', context)

    def post(self, request):
        pass

