from django.views.generic import TemplateView


class Profile(TemplateView):
    template_name = 'account/profile_page.html'
