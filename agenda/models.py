from django.db import models


class Agenda(models.Model):
    title = models.CharField(max_length=50, verbose_name='日程标题')
    description = models.CharField(max_length=256, verbose_name='简介', blank=True)
    userID = models.IntegerField(verbose_name='创建人ID')
    groupID = models.IntegerField(verbose_name='组ID')
    priority_level = models.PositiveSmallIntegerField(verbose_name='优先级', default=1)
    start_time = models.DateTimeField(verbose_name='开始时间')
    last_time = models.TimeField(verbose_name='预计时长')

    class Meta:
        verbose_name = '日程'
        verbose_name_plural = verbose_name



