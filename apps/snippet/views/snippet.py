from django.shortcuts import render
from django.views.generic import View

from apps.snippet.models import Snippet


class SnippetView(View):

    def get(self, request, username, uid):
        context = dict()
        snippet = Snippet.objects.all().filter(uid=uid).prefetch_related('language', 'author').first()
        context['snippet'] = snippet
        return render(request, 'snippet/snippet.html', context)

    def post(self, request):
        pass

