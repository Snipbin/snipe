from django.shortcuts import render
from django.views.generic import View

from apps.core.models import Language


class Home(View):
    homepage = 'core/index.html'

    def get(self, request):
        context = dict()
        context['all_languages'] = Language.objects.all().order_by('name')
        return render(request, self.homepage, context)

    def post(self, request):
        pass
