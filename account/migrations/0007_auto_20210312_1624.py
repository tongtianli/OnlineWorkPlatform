# Generated by Django 3.1.4 on 2021-03-12 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20210310_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workgroup',
            name='name',
            field=models.CharField(max_length=60, verbose_name='组名'),
        ),
    ]
