# Generated by Django 3.1.4 on 2021-05-13 11:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kbase', '0006_auto_20210513_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 13, 19, 13, 31, 677942), verbose_name='创建时间'),
        ),
    ]
