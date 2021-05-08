from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Agenda(models.Model):
    title = models.CharField(max_length=50, verbose_name='日程标题')
    description = models.CharField(max_length=256, verbose_name='简介', blank=True)
    userID = models.IntegerField(verbose_name='创建人ID', default=-1)
    groupID = models.IntegerField(verbose_name='组ID', default=-1)
    priority_level = models.PositiveSmallIntegerField(verbose_name='优先级', default=1)
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')

    class Meta:
        verbose_name = '日程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Participant(models.Model):
    agenda = models.ForeignKey(Agenda, verbose_name='日程', related_name='participants', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='人员', related_name='related_agenda', on_delete=models.CASCADE)
