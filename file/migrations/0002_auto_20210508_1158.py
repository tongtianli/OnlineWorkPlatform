# Generated by Django 3.1.4 on 2021-05-08 03:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 8, 11, 58, 46, 186420), verbose_name='创建日期'),
        ),
    ]