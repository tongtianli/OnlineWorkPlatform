# Generated by Django 3.1.4 on 2021-05-17 03:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0009_auto_20210515_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 17, 11, 32, 59, 576056), verbose_name='创建日期'),
        ),
    ]
