from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForm(forms.Form):
    # 유저가 로그인 할 경우 이메일과 비밀번호를 입력하고 접속
    email = forms.EmailField()
    # 위젯을 사용하여 패스워드를 점 형태로 바꿔준다.
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                # raise 대신 오류 알림을 발생시키고자 하는 방법(한 필드에 직접 에러를 추가해야 한다.)
                self.add_error(
                    "password", forms.ValidationError("비밀번호가 틀렸습니다.(Password is wrong)")
                )

        except models.User.DoesNotExist:
            self.add_error(
                "email", forms.ValidationError("유저가 존재하지 않습니다.(User doesn't exist)")
            )


class SignUpForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()

