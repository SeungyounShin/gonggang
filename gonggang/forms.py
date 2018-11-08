from django import forms

from django import forms

class everytimeSubmit(forms.Form):
    everytime_id = forms.CharField(label='에브리타임 아이디', max_length=30)
    everytime_pw = forms.CharField(label='에브리타임 비밀번호', max_length=30)
