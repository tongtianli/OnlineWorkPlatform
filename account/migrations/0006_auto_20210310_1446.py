# Generated by Django 3.1.4 on 2021-03-10 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20210302_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workgroup',
            name='leader',
        ),
        migrations.AddField(
            model_name='workgroup',
            name='leaderID',
            field=models.IntegerField(default=1, verbose_name='组长'),
            preserve_default=False,
        ),
    ]