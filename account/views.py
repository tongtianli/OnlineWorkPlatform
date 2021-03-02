from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponseRedirect
from django.views import View

from account.forms import UserCreationForm, UserLoginForm
from .models import User


class CreateUserView(View):
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
