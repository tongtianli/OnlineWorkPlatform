from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Mail(models.Model):
    sender = models.ForeignKey(User, verbose_name='发送人', related_name='sent_mails', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, verbose_name='接收人', related_name='received_mails', on_delete=models.CASCADE)
    about = models.CharField(max_length=20, verbose_name='主题')
    text = models.CharField(max_length=50, verbose_name='正文')
    read = models.BooleanField(verbose_name='是否已读', default=False)
    create_time = models.DateTimeField(verbose_name='发送时间', default=datetime.now())

    class Meta:
        verbose_name = '站内信'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.about


# 在主页显示的，阅读即销毁的短消息
class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='目标用户', related_name='messages')
    # 1-新日程 2-新知识库 3-新文件 4-新站内信 0-系统消息
    type = models.SmallIntegerField(verbose_name='类型')
    create_time = models.DateTimeField(verbose_name='时间', default=datetime.now())
    item_id = models.IntegerField(verbose_name='内容id', blank=True, null=True)
    content = models.CharField(verbose_name='文字描述', max_length=50)
    involved = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='涉及用户', blank=True, null=True)
