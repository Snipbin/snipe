from django.shortcuts import render, redirect
from django.views import View


class HomeView(View):
    homepage = 'core/home.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, self.homepage, {})
