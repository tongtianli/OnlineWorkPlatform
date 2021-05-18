import json
from datetime import datetime

from django import http
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View

from mail.models import Message
from .forms import AgendaForm
from .models import Agenda, Participant

User = get_user_model()


class AgendaView(LoginRequiredMixin, View):
    def get(self, request):
        personal_agenda = Agenda.objects.filter(userID=request.user.id, groupID=-1)
        if request.user.groupID != -1:
            group_agenda = Agenda.objects.filter(groupID=request.user.groupID)
        return render(request, 'agenda/agenda.html', locals())


class AgendaCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'agenda/add-agenda.html')

    def post(self, request):
        res = dict(result=False)
        form = AgendaForm(request.POST)
        if form.is_valid():
            form.save()
            res['result'] = True
        return http.HttpResponse(json.dumps(res), content_type='application/json')


class AgendaDetialView(LoginRequiredMixin, View):
    def get(self, request, agenda_id):
        agenda = get_object_or_404(Agenda, pk=agenda_id)
        user = get_object_or_404(User, pk=agenda.userID)
        return render(request, 'agenda/agenda-detail.html', locals())

    def post(self, request, agenda_id):
        res = dict(result=False)
        form = AgendaForm(request.POST)
        if form.is_valid():
            origin = get_object_or_404(Agenda, pk=agenda_id)
            origin.title = form.cleaned_data['title']
            origin.start_time = form.cleaned_data['start_time']
            origin.end_time = form.cleaned_data['end_time']
            origin.description = form.cleaned_data['description']
            origin.priority_level = form.cleaned_data['priority_level']
            origin.save()
            res['result'] = True
        return http.HttpResponse(json.dumps(res), content_type='application/json')


class GroupAgendaCreateView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.filter(groupID=request.user.groupID)
        return render(request, 'agenda/add-group-agenda.html', locals())

    def post(self, request):
        res = dict(result=False)
        form = AgendaForm(request.POST)
        if form.is_valid():
            participants = request.POST.getlist('participants')
            agenda = form.save()
            res['result'] = True
            if participants:
                for participant in participants:
                    user = get_object_or_404(User, email=participant)
                    p = Participant(agenda=agenda, user=user)
                    p.save()
                    Message(owner=user, type=1, item_id=agenda.id, content=agenda.title, involved=request.user).save()
            else:
                group_users = User.objects.filter(groupID=request.user.groupID)
                for user in group_users:
                    p = Participant(agenda=agenda, user=user)
                    p.save()
                    Message(owner=user, type=1, item_id=agenda.id, content=agenda.title, involved=request.user).save()
        return http.HttpResponse(json.dumps(res), content_type='application/json')


class ConflictView(LoginRequiredMixin, View):
    def post(self, request):
        participants = request.POST.getlist('participants')
        form = AgendaForm(request.POST)
        conflict = dict()
        if form.is_valid():
            agenda = form.save(commit=False)
            print(type(agenda.start_time))
            if participants:
                for participant in participants:
                    user = get_object_or_404(User, email=participant)
                    conflict_agenda = Agenda.objects.filter(userID=user.id, groupID=-1, start_time__lt=agenda.end_time,
                                                            end_time__gte=agenda.start_time)
                    if conflict_agenda:
                        conflict[user] = conflict_agenda
            else:
                for user in User.objects.filter(groupID=request.user.groupID):
                    conflict_agenda = Agenda.objects.filter(userID=user.id, groupID=-1, start_time__lt=agenda.end_time,
                                                            end_time__gte=agenda.start_time)
                    if conflict_agenda:
                        conflict[user] = conflict_agenda
            return render(request, 'agenda/conflict.html',
                          {'new_agenda': agenda, 'conflict': conflict, 'participants': participants})
        return http.HttpResponse('请正确填写')


def deleteAgenda(request):
    res = dict(result=False)
    userID = int(request.POST.get('userID'))
    agendaID = int(request.POST.get('agendaID'))
    agenda = get_object_or_404(Agenda, pk=agendaID)
    if agenda.userID == userID:
        agenda.delete()
        res['result'] = True
    return http.HttpResponse(json.dumps(res), content_type='application/json')
