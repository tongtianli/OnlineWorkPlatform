# Generated by Django 3.1.4 on 2021-03-13 06:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kbase', '0002_auto_20210313_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 14, 9, 56, 712357), verbose_name='创建时间'),
        ),
    ]
