from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect
from django.views import View

from .models import User


class CreateUserView(View):
    def get(self, request):
        return render(request, 'account/create-user.html')

    def post(self, request):
        email = request.POST.get("inputEmail")
        password = request.POST.get("inputPassword")
        password2 = request.POST.get("inputPassword2")
        if email and password and password2:
            if password == password2:
                user = User.objects(Q(email=email))
                if not user:
                    user = User(email=email, password=password)
                    user.save()
                    return HttpResponseRedirect('/')
                else:
                    return render(request, 'account/create-user.html', {'msg': '该邮箱已经注册'})
            else:
                return render(request, 'account/create-user.html', {'msg': '两次输入的密码不一致'})
        else:
            return render(request, 'account/create-user.html', {'msg': '请填写全部字段'})


class LoginView(View):
    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):
        email = request.POST.get("inputEmail")
        password = request.POST.get("inputPassword")
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
