# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-27 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_auto_20191027_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid1', models.IntegerField()),
                ('uid2', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='swiped',
            name='stime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='滑动时间'),
        ),
    ]
