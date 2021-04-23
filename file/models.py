from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

from account.models import WorkGroup

User = get_user_model()


class Path(models.Model):
    name = models.TextField(verbose_name='路径名')
    groupID = models.IntegerField(verbose_name='所属组')
    is_root = models.BooleanField(verbose_name='是否为根', default=False)
    parent = models.IntegerField(verbose_name='上级目录', default=-1)


class File(models.Model):
    name = models.TextField(verbose_name='文件名')
    parent = models.IntegerField(verbose_name='所属文件夹')
    file = models.FileField(verbose_name='服务器路径')
    groupID = models.IntegerField(verbose_name='所属组')
    owner = models.EmailField(verbose_name='创建人')
    download = models.PositiveIntegerField(verbose_name='下载量', default=0)
    create_time = models.DateTimeField(default=datetime.now(), verbose_name='创建日期')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name


class FileSystem(models.Model):
    group = models.OneToOneField(WorkGroup, on_delete=models.CASCADE, verbose_name='组文件', related_name='files')
    root_path_id = models.IntegerField(verbose_name='根节点ID')
    file_count = models.PositiveIntegerField(verbose_name='文件数量')
    file_size_count = models.PositiveIntegerField(verbose_name='文件总大小')
    file_limit = models.PositiveIntegerField(verbose_name='组文件大小限制', default=104857600)  # 100MB容量限制
