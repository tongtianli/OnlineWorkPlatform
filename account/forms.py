from django import forms

from .models import WorkGroup


class UserCreationForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '电子邮箱'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}))
    repeat = forms.CharField(label='重复密码',
                             widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '重复密码'}))


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '电子邮箱'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}))


class WorkGroupForm(forms.ModelForm):
    create_time = forms.DateTimeField(required=False)

    class Meta:
        model = WorkGroup
        fields = '__all__'
