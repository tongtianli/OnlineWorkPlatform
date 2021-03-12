# Generated by Django 3.1.4 on 2021-03-12 08:24

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('body', models.TextField(verbose_name='正文')),
                ('create_time', models.DateTimeField(default=datetime.datetime(2021, 3, 12, 16, 24, 50, 164683), verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('read_times', models.PositiveIntegerField(verbose_name='浏览量')),
                ('likes', models.PositiveIntegerField(verbose_name='点赞数')),
                ('comments', models.PositiveIntegerField(verbose_name='评论数')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('create_time',),
            },
        ),
    ]