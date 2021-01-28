from django.contrib.auth import get_user_model
from django.db import models

from account.models import WorkGroup


class PersonalAgenda(models.Model):
    title = models.CharField(max_length=50, verbose_name='日程标题')
    description = models.CharField(max_length=256, verbose_name='简介', blank=True)
    owner = models.ForeignKey(get_user_model(), related_name='personal_agenda', on_delete=models.CASCADE,
                              verbose_name='所有者')
    priority_level = models.PositiveSmallIntegerField(verbose_name='优先级', default=1)
    start_time = models.DateTimeField(verbose_name='开始时间')
    last_time = models.TimeField(verbose_name='预计时长')

    class Meta:
        verbose_name = '个人日程'
        verbose_name_plural = verbose_name


class GroupAgenda(models.Model):
    title = models.CharField(max_length=50, verbose_name='组日程标题')
    description = models.CharField(max_length=256, verbose_name='组日程说明')
    owner = models.ForeignKey(get_user_model(), verbose_name='发起人', on_delete=models.DO_NOTHING)
    ownerGroup = models.ForeignKey(WorkGroup, related_name='group_agenda', on_delete=models.CASCADE, verbose_name='属于组')
    member = models.ManyToManyField(get_user_model(), verbose_name='参加人员', blank=True)
    start_time = models.DateTimeField(verbose_name='组日程开始时间')
    last_time = models.TimeField(verbose_name='组日程持续时间')

    class Meta:
        verbose_name = '团队日程'
        verbose_name_plural = verbose_name
