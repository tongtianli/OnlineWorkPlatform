from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='标题')
    body = models.TextField(verbose_name='正文')
    create_time = models.DateTimeField(default=datetime.now(), verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    read_times = models.PositiveIntegerField(verbose_name='浏览量', default=0)
    likes = models.PositiveIntegerField(verbose_name='点赞数', default=0)
    comments = models.PositiveIntegerField(verbose_name='评论数', default=0)

    class Meta:
        ordering = ('create_time',)

    def __str__(self):
        return self.title
