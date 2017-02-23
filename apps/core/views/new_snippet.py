from django.utils import timezone
from django.shortcuts import render
from django.views.generic import View

from apps.account.models import UserProfile
from apps.core.models import Language
from apps.snippet.models import Snippet


class NewSnippet(View):
    homepage = 'core/index.html'

    def get(self, request):
        context = dict()
        context['all_languages'] = Language.objects.all().order_by('name')
        return render(request, self.homepage, context)

    def post(self, request):
        context = dict()
        context['errors'] = list()
        post_data = request.POST.dict()
        if post_data['title'] == '':
            context['errors'].append("Error: No title specified.")
        if post_data['code'] == '':
            context['errors'].append("Error: This doesn't contain any code.")

        if len(context['errors']) == 0:
            snippet_created_date = timezone.now()
            snippet_expiry_date = timezone.now()
            if post_data['expiry'] == 0:
                snippet_expiry_date += timezone.timedelta(days=9999999999)  # ToDo: Make this more robust
            else:
                snippet_expiry_date += timezone.timedelta(days=int(post_data['expiry']))
            snippet_is_private = False
            if post_data['privacy']:
                snippet_is_private = True
            snippet = Snippet(
                title=post_data['title'],
                language=Language.objects.all().filter(id=int(post_data['language']))[0],
                code=post_data['code'],
                author=UserProfile.objects.all().filter(id=1)[0],
                is_private=snippet_is_private,
                created_at=snippet_created_date,
                last_modified=snippet_created_date,
                expiry_date=snippet_expiry_date,
            )
            snippet.save()

        return render(request, self.homepage, context)