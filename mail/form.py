from django import forms

from .models import Mail


class MailForm(forms.ModelForm):
    receiver_name = forms.CharField(max_length=256)

    class Meta:
        model = Mail
        fields = ('about', 'text')
