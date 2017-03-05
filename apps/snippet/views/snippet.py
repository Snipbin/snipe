from uuid import UUID

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View

from apps.snippet.models import Snippet


class SnippetView(LoginRequiredMixin, View):
    snippet_page = 'snippet/snippet.html'
    error_404_page = '404.html'
    login_url = '/auth/login/'
    redirect_field_name = 'redirect'

    def get(self, request, username, uid):
        context = dict()
        if self.is_valid_uuid(uid):
            snippet = Snippet.objects.all().filter(
                uid=uid, author__user__username=username
            ).prefetch_related('language', 'author').first()
            if snippet is not None:
                context['snippet'] = snippet
                return render(request, self.snippet_page, context)
        else:
            return render(request, self.error_404_page, context)

    def post(self, request):
        pass

    @staticmethod
    def is_valid_uuid(uuid_to_test, version=4):
        try:
            uuid_obj = UUID(uuid_to_test, version=version)
        except ValueError:
            return False

        return str(uuid_obj).replace('-', '') == uuid_to_test
