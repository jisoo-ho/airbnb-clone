from django import forms
from . import models


class LoginForm(forms.Form):
    # 유저가 로그인 할 경우 이메일과 비밀번호를 입력하고 접속
    email = forms.EmailField()
    # 위젯을 사용하여 패스워드를 점 형태로 바꿔준다.
    password = forms.CharField(widget=forms.PasswordInput)

    # 내부 함수를 사용한 것(clean_email, password는 임시로 지정한 명칭이 아니다.)
    # 전달받은 이메일과 비밀번호가 에러가 없을 경우 views.py에서 is_valid()가 True로 작동
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("유저가 존재하지 않습니다.(User doesn't exist)")

    def clean_password(self):
        return "lalalalalalal"
