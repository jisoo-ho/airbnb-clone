from django.views import View
from django.shortcuts import render
from . import forms


class LoginView(View):
    """클래스 기반 뷰"""

    def get(self, request):
        form = forms.LoginForm(initial={"email": "itn@las.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)  # 모든 필드를 정리해준 결과
        return render(request, "users/login.html", {"form": form})
