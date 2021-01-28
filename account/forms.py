from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from account.models import User


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': ('两次输入的密码不一致'),
    }
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    repeat = forms.CharField(label='重复密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
