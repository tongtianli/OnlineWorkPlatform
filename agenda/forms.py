from django import forms

from .models import Agenda


class AgendaForm(forms.ModelForm):
    userID = forms.IntegerField(required=False)
    groupID = forms.IntegerField(required=False)

    class Meta:
        model = Agenda
        fields = '__all__'

class GroupAgendaForm(forms.ModelForm):
    userID = forms.IntegerField(required=False)
    groupID = forms.IntegerField(required=False)
    participants = forms.CharField()

    class Meta:
        model = Agenda
        fields = '__all__'