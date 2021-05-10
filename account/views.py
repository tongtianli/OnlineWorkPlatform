import json
from datetime import datetime

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.views import View

from account.forms import UserCreationForm, UserLoginForm, WorkGroupForm, AvatarForm, AnnouncementForm
from account.models import WorkGroup, Confirmation, GroupInvitation

User = get_user_model()


class AccountView(LoginRequiredMixin, View):
    def get(self, request):
        group = None
        if WorkGroup.objects.filter(pk=request.user.groupID):
            group = WorkGroup.objects.get(pk=request.user.groupID)
        return render(request, 'account/account.html', {'group': group})


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
        next = request.GET.get('next', '/')
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            auth = authenticate(request, username=email, password=password)
            if auth is not None:
                login(request, auth)
                return HttpResponseRedirect(next)
            else:
                return render(request, 'account/login.html', {'msg': '请检查邮箱和密码是否正确'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class GroupView(LoginRequiredMixin, View):
    def get(self, request):
        group = None
        group_users = None
        all_nongroup_users = User.objects.filter(groupID=-1)
        if request.user.groupID != -1:
            group = get_object_or_404(WorkGroup, pk=request.user.groupID)
            group_users = User.objects.filter(groupID=group.id)
        return render(request, 'account/group.html', locals())


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


class AvatarChangeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'account/change-avatar.html')

    def post(self, request):
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid() and 'avatar' in request.FILES:
            user = request.user
            user.avatar = form.cleaned_data['avatar']
            user.save()


class HomePageView(LoginRequiredMixin, View):
    def get(self, request, id):
        user = get_object_or_404(User, pk=id)
        return render(request, 'account/homepage.html', {'user': user})


class AnnounceCreateView(LoginRequiredMixin, View):
    def get(self, request):
        group = get_object_or_404(WorkGroup, pk=request.user.groupID)
        if group.leaderID != request.user.id:
            return HttpResponse('你必须是组管理者才能添加公告')
        return render(request, 'account/group-announcement.html')

    def post(self, request):
        res = dict(result=False)
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class AnnounceConfirmView(LoginRequiredMixin, View):
    def post(self, request, announce_id):
        confirm = Confirmation(announcement_id=announce_id, user=request.user)
        confirm.save()
        return redirect('account:group')


class GroupInviteView(LoginRequiredMixin, View):
    def post(self, request):
        group = get_object_or_404(WorkGroup, pk=request.POST.get('group'))
        user = get_object_or_404(User, email=request.POST.get('invitedUser'))
        if not GroupInvitation.objects.filter(group=group, invitedUser=user):
            i = GroupInvitation(group=group, invitedUser=user)
            i.save()
            return redirect('account:group')
        else:
            return HttpResponse('请不要重复发送请求')


class GroupAcceptView(LoginRequiredMixin, View):
    def post(self, request):
        if request.user.groupID != -1:
            return HttpResponse('你已经在小组里了，如果要加入其他组请退组')
        group = get_object_or_404(WorkGroup, pk=request.POST.get('group'))
        user = request.user
        user.groupID = group.id
        user.save()
        return redirect("account:group")


class InviteCancelView(LoginRequiredMixin, View):
    def post(self, request):
        invite = get_object_or_404(GroupInvitation, pk=request.POST.get('invite'))
        invite.delete()
        return redirect("account:group")
