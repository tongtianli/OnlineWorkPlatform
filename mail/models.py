from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Mail(models.Model):
    sender = models.EmailField(verbose_name='发送人')
    receiver = models.EmailField(verbose_name='接收人')
    about = models.CharField(max_length=20, verbose_name='主题')
    text = models.CharField(max_length=50, verbose_name='正文')
    read = models.BooleanField(verbose_name='是否已读', default=False)
    create_time = models.DateTimeField(verbose_name='发送时间', default=datetime.now())

    class Meta:
        verbose_name = '站内信'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.about
