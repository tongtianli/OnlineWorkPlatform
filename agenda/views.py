from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .models import Agenda


class AgendaView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        uid = user.id
        gid = user.groupID
        personal_agenda = Agenda.objects.filter(userID=uid)
        group_agenda = Agenda.objects.filter(groupID=gid)

        return render(request, 'agenda/agenda.html')
