from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import View

from apps.core.models import Language
from apps.snippet.models import Snippet


class SnippetEditView(LoginRequiredMixin, View):

    edit_page = 'snippet/edit.html'
    snippet_page = 'snippet/view.html'

    def get(self, request, username, uid):
        context = dict()
        context['all_languages'] = Language.objects.all().order_by('name')
        snippet = Snippet.objects.all().filter(uid=uid, author__username=username).first()
        if snippet.author == request.user:
            context['snippet'] = snippet
            return render(request, self.edit_page, context)
        else:
            return HttpResponseForbidden()

    def post(self, request, username, uid):
        context = dict()
        context['errors'] = list()
        context['all_languages'] = Language.objects.all().order_by('name')
        post_data = request.POST.dict()
        if post_data['title'] == '':
            context['errors'].append("Error: No title specified.")
        if post_data['code'] == '':
            context['errors'].append("Error: This doesn't contain any code.")

        snippet = Snippet.objects.all().filter(uid=uid,
                                               author__username=username).first()
        if len(context['errors']) == 0:
            if snippet.author == request.user:
                snippet_modified_date = timezone.now()
                snippet_expiry_date = timezone.now()
                if post_data['expiry'] == 0:
                    snippet_expiry_date += timezone.timedelta(days=9999999999)  # ToDo: Make this more robust
                else:
                    snippet_expiry_date += timezone.timedelta(days=int(post_data['expiry']))
                if post_data['privacy'] == "public":
                    snippet_is_private = 'PUBLIC'
                elif post_data['privacy'] == "link":
                    snippet_is_private = 'LINK'
                else:
                    snippet_is_private = 'PRIVATE'
                snippet.title = post_data['title']
                snippet.description = post_data['description']
                snippet.language = Language.objects.all().filter(id=int(post_data['language'])).first()
                snippet.code = post_data['code']
                snippet.is_private = snippet_is_private
                snippet.last_modified = snippet_modified_date
                snippet.expiry_date = snippet_expiry_date
                snippet.save()
                return redirect('snippet:snippet', username=snippet.author.username, uid=snippet.uid.hex)
            else:
                return HttpResponseForbidden()

        context['snippet'] = snippet
        return render(request, self.edit_page, context)
