from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class WorkGroup(models.Model):
    name = models.CharField(max_length=60, verbose_name="工作组")
    leader = models.EmailField(max_length=50, verbose_name="组长")
    introduction = models.CharField(max_length=256, verbose_name="简介")
    create_time = models.DateField(verbose_name="组创建日期", default=timezone.now)

    class Meta:
        verbose_name = "工作组"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('用户必须提供电子邮箱')
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self.db)
        return user


class User(AbstractUser):
    email = models.EmailField(max_length=50, verbose_name="邮箱", unique=True)

    nickname = models.CharField(max_length=20, default="", verbose_name="昵称", blank=True)
    name = models.CharField(max_length=20, default="", verbose_name="姓名", blank=True)
    avatar = models.ImageField(upload_to="avatar", default="avatar/default.png", verbose_name="头像")

    objects = UserManager()

    groupID = models.IntegerField(verbose_name='组序号', default=-1)

    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
