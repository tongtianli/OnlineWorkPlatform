from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .form import *

User = get_user_model()


class MailView(LoginRequiredMixin, View):
    def get(self, request):
        mails = Mail.objects.filter(receiver=request.user.email)
        send_mails = Mail.objects.filter(sender=request.user.email)
        return render(request, 'mail/mail.html', locals())

    def post(self, request):
        form = MailForm(request.POST)
        if form.is_valid():
            new_mail = form.save(commit=False)
            new_mail.sender = request.user.email
            new_mail.save()
            return redirect('mail:main')
        else:
            return HttpResponse('请输入正确的邮箱')