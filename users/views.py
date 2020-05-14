from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(View):
    """클래스 기반 뷰"""

    def get(self, request):
        form = forms.LoginForm(initial={"email": "itn@las.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            # authenticate : django가 쿠키 관리와 DB 연결을 자동으로 해준다.
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))  # 로그인 완료시 홈 화면으로 이동
                # 관리자가 로그인 한 경우 admin 페이지까지 함께 로그인 완료 처리

        return render(request, "users/login.html", {"form": form})


# 로그아웃 메서드(로그아웃 시 홈으로 이동)
def log_out(request):
    logout(request)  # 이 줄의 로그아웃은 임포트한 함수이므로 주의
    return redirect(reverse("core:home"))
