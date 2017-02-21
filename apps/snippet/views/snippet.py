from django.shortcuts import render
from django.views.generic import View


class Snippet(View):

    def get(self, request):
        return render(request, 'snippet/snippet.html')

    def post(self, request):
        pass

