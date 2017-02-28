from django.shortcuts import render
from django.views import View

from apps.snippet.models import Snippet


class DiscoverView(View):
    discover_page = 'snippet/discover.html'

    def get(self, request):
        context = dict()
        snippets = Snippet.objects.all().order_by('last_modified')
        print(snippets)
        context['snippets'] = snippets
        return render(request, self.discover_page, context)

    def post(self, request):
        pass
