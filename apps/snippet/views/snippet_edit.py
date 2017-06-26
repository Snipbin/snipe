from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import View

from apps.core.models import Language
from apps.snippet.models import Snippet
from apps.snippet.serializers import SnippetEditSerializer


class SnippetEditView(LoginRequiredMixin, View):

    edit_page = 'snippet/edit.html'
    snippet_page = 'snippet/view.html'

    def get(self, request, uid):
        context = dict()
        context['all_languages'] = Language.objects.order_by('name')
        snippet: Snippet = Snippet.objects.all().filter(uid=uid).first()
        if not snippet:
            raise Http404()
        if snippet.author_id == request.user.id:
            context['snippet'] = snippet
            return render(request, self.edit_page, context)
        else:
            return HttpResponseForbidden()

    def post(self, request, uid):

        snippet: Snippet = Snippet.objects.all().filter(uid=uid).first()
        if not snippet:
            raise Http404()

        if snippet.author_id != request.user.id:
            return HttpResponseForbidden()

        context = dict()
        context['errors'] = list()
        context['all_languages'] = Language.objects.order_by('name')

        serialized_data = SnippetEditSerializer(data=request.POST, instance=snippet)
        if serialized_data.is_valid():
            snippet_expiry_date = timezone.now()
            expiry_field = serialized_data.validated_data['expiry']
            if expiry_field == 0:
                snippet_expiry_date += timezone.timedelta(days=999999)  # ToDo: Make this more robust
            else:
                snippet_expiry_date += timezone.timedelta(days=expiry_field)
            serialized_data.save(expiry_date=snippet_expiry_date, last_modified=timezone.now())
            return redirect('snippet:snippet', uid=snippet.uid.hex)
        else:
            context['errors'] = serialized_data.errors

        context['snippet'] = snippet
        return render(request, self.edit_page, context)
