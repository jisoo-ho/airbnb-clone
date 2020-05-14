from django import forms
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


class SignUpForm(forms.Form):

    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "이미 존재하는 이메일 입니다.(User already exists with that email)"
            )
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):  # 양식의 필드를 순차적으로 clean하기 때문에 명칭을 다르게 한다.
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError(
                "비밀번호가 일치하지 않습니다.(Password confirmation does not match)"
            )
        else:
            return password

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = models.User.objects.create_user(email, email, password)  # 암호화 하여 저장
        user.first_name = first_name
        user.last_name = last_name
        user.save()
