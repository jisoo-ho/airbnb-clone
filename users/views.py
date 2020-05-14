from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


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
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
