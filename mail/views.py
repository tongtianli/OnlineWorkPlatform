from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .form import *
from .models import Message

User = get_user_model()


class MailView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'mail/mail.html')

    def post(self, request):
        form = MailForm(request.POST)
        if form.is_valid():
            new_mail = form.save(commit=False)
            new_mail.sender = request.user.email
            r = form.cleaned_data['receiver_name']
            if r=='小组':
                if request.user.groupID == -1:
                    return HttpResponse('你还没有小组')
                else:
                    for user in User.objects.filter(groupID=request.user.groupID):
                        if user != request.user:
                            new_mail.receiver = user
                            new_mail.save()
                            Message(owner=new_mail.receiver, type=4, item_id=new_mail.id, content=new_mail.about,
                                    involved=request.user).save()
                    return redirect('mail:main')
            else:
                if User.objects.filter(email=r):
                    new_mail.receiver = User.objects.get(email=r)
                    new_mail.save()
                    Message(owner=new_mail.receiver, type=4, item_id=new_mail.id, content=new_mail.about,
                            involved=request.user).save()
                    return redirect('mail:main')
                else:
                    return HttpResponse('无此用户，站内信发送失败')


class MessageDeleteView(LoginRequiredMixin, View):
    def get(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        message.delete()
        return HttpResponse('OK')
