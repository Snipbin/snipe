from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.generic import View

from apps.account.models import SnipeUser
from apps.core.models import Language
from apps.snippet.models import Snippet


class NewSnippetView(LoginRequiredMixin, View):
    homepage = 'core/index.html'
    login_url = '/auth/login/'
    redirect_field_name = 'redirect'

    @staticmethod
    def __build_context():
        context = dict()
        context['all_languages'] = Language.objects.all().order_by('name')
        return context

    def get(self, request):
        context = self.__build_context()
        return render(request, self.homepage, context)

    def post(self, request):
        context = self.__build_context()
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
            if post_data['privacy'] == "public":
                snippet_is_private = 'PUBLIC'
            elif post_data['privacy'] == "link":
                snippet_is_private = 'LINK'
            else:
                snippet_is_private = 'PRIVATE'
            snippet = Snippet(
                title=post_data['title'],
                language=Language.objects.all().filter(id=int(post_data['language'])).first(),
                description=post_data['description'],
                code=post_data['code'],
                author=SnipeUser.objects.all().filter(id=1).first(),
                is_private=snippet_is_private,
                created_at=snippet_created_date,
                last_modified=snippet_created_date,
                expiry_date=snippet_expiry_date,
            )
            snippet.save()

            return redirect('snippet:snippet', username=snippet.author.user.username, uid=snippet.uid.hex)

        return render(request, self.homepage, context)
