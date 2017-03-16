from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import View

from apps.snippet.models import Snippet


class SnippetDeleteView(LoginRequiredMixin, View):

    def get(self, request):
        pass

    def post(self, request):
        post_data = request.POST.dict()
        if post_data['uid'] == '':
            return redirect('snippet:new')
        else:
            snippet = Snippet.objects.all().filter(uid=post_data['uid']).first()
            if request.user == snippet.author:
                snippet.delete()
        return redirect('snippet:new')
