from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.views.generic import View

from apps.snippet.models import Snippet


class SnippetDeleteView(LoginRequiredMixin, View):

    def post(self, request, uid):
        snippet = Snippet.objects.all().filter(uid=uid).first()
        if request.user.id == snippet.author_id:
            snippet.delete()
        else:
            return HttpResponseForbidden()
        return redirect('snippet:new')
