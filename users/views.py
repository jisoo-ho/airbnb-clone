from django.views import View
from django.shortcuts import render
from . import forms


class LoginView(View):
    """클래스 기반 뷰"""

    def get(self, request):
        form = forms.LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        print(form)
