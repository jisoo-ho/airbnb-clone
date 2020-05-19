import os
import requests
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models


class LoginView(FormView):
    """ 뷰를 불러올 때 URL이 불려지지 않았다. 
    이를 위해 reverse_lazy를 사용(lazy는 실행하지 않는다는 의미, 필요할 경우에 사용됨) """

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")  # 홈으로 이동

    def form_valid(self, form):  # form_valid 함수를 이용해서 유효한지 체크
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)  # 이 때(로그인 성공시) success_url로 이동하고 모두 작동


# 로그아웃 메서드(로그아웃 시 홈으로 이동)
def log_out(request):
    logout(request)  # 이 줄의 로그아웃은 임포트한 함수이므로 주의
    return redirect(reverse("core:home"))


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")  # 회원가입 성공 시 이동 화면(홈)
    initial = {"first_name": "jisoo", "last_name": "ho", "email": "hojysoo@naver.com"}

    def form_valid(self, form):
        form.save()  # 저장 함수 실행
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:  # user가 로그인 되었다면
            login(self.request, user)
        user.verify_email()  # 이메일 전송하여 인증
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""  # 이메일 시크릿 키 삭제(공백으로 재 설정)
        user.save()
        # 성공 메시지 추가할 것
    except models.User.DoesNotExist:
        # 에러 메시지 추가할 것
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    client_id = os.environ.get("GH_ID")
    client_secret = os.environ.get("GH_SECRET")
    code = request.GET.get("code", None)
    if code is not None:
        request = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
            headers={"Accept": "application/json"},
        )  # 설정해놓은 ID, PW를 URL로 보낸다.(requests lib)
        print(request.json())
    else:
        return redirect(reverse("core:home"))
