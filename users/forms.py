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


class SignUpForm(forms.ModelForm):  # ModelForm이 이메일과 이름을 대신해서 생성
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_password1(self):  # 양식의 필드를 순차적으로 clean하기 때문에 명칭을 다르게 한다.
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError(
                "비밀번호가 일치하지 않습니다.(Password confirmation does not match)"
            )
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)  # object는 생성하지만 DB에는 포함하지 않는다.
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()  # commit=True 기본값
