import json
from datetime import datetime

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views import View

from account.forms import UserCreationForm, UserLoginForm, WorkGroupForm
from account.models import WorkGroup

User = get_user_model()


class AccountView(LoginRequiredMixin, View):
    def get(self, request):
        group = get_object_or_404(WorkGroup, pk=request.user.groupID)
        return render(request, 'account/account.html',{'group':group})


class UserCreateView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'account/create-user.html', locals())

    def post(self, request):
        form = UserCreationForm(request.POST)
        msg = '出错了'
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['repeat']
            if password == password2:
                user = User.objects.filter(email=email)
                if len(user) > 0:
                    msg = '该邮箱已经注册'
                else:
                    user = User(email=email, username=email, password=password)
                    user.save()
                    return HttpResponseRedirect('/')
            else:
                msg = '两次输入的密码不一致'
        return render(request, 'account/create-user.html', locals())


class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'account/login.html', locals())

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            auth = authenticate(request, username=email, password=password)
            if auth is not None:
                login(request, auth)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'account/login.html', {'msg': '请检查邮箱和密码是否正确'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class GroupView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        group = None
        group_users = None
        if user.groupID != -1:
            group = get_object_or_404(WorkGroup, pk=user.groupID)
            group_users = User.objects.filter(groupID=group.id)
        return render(request, 'account/group.html', {'group': group, 'group_users': group_users})


class GroupJoinView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'account/join-group.html')


class GroupCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'account/create-group.html')

    def post(self, request):
        res = dict(result=False)
        form = WorkGroupForm(request.POST)
        if form.is_valid():
            form.create_time = datetime.now()
            form.save()
            leaderID = form.cleaned_data['leaderID']
            user = get_object_or_404(User, pk=leaderID)
            group = get_object_or_404(WorkGroup, leaderID=leaderID)
            user.groupID = group.id
            user.save()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')
