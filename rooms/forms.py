from django import forms
from . import models


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")
    price = forms.IntegerField(required=False)
    # ModelChoiceField 을 통해 select 태그 값 삽입 가능
    room_type = forms.ModelChoiceField(queryset=models.RoomType.objects.all())
