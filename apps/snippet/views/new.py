from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View

from apps.core.models import Language
from apps.snippet.serializers import SnippetEditSerializer


class NewSnippetView(LoginRequiredMixin, View):
    homepage = 'snippet/new.html'

    @staticmethod
    def _build_context():
        context = dict()
        context['all_languages'] = Language.objects.all().order_by('name')
        return context

    def get(self, request):
        context = self._build_context()
        return render(request, self.homepage, context)

    def post(self, request):
        context = self._build_context()
        context['errors'] = list()

        serialized_data = SnippetEditSerializer(data=request.POST)
        if serialized_data.is_valid():
            snippet_expiry_date = timezone.now()
            expiry_field = serialized_data.validated_data['expiry']
            if expiry_field == 0:
                snippet_expiry_date += timezone.timedelta(days=999999)  # ToDo: Make this more robust
            else:
                snippet_expiry_date += timezone.timedelta(days=expiry_field)
            snippet = serialized_data.save(
                author=request.user,
                created_at=timezone.now(),
                expiry_date=snippet_expiry_date,
                last_modified=timezone.now(),
            )
            return redirect('snippet:snippet', uid=snippet.uid.hex)

        else:
            context['errors'] = serialized_data.errors

        return render(request, self.homepage, context)
