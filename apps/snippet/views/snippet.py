from django.views.generic import TemplateView


class Snippet(TemplateView):
    template_name = 'snippet/snippet.html'
