from django import forms


class FileForm(forms.Form):
    file = forms.FileField()


class PathForm(forms.Form):
    folder = forms.CharField()

