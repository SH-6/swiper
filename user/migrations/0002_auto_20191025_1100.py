# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-25 03:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dating_sex', models.CharField(choices=[('male', '男性'), ('male', '女性')], max_length=16, verbose_name='匹配的性别')),
                ('location', models.CharField(choices=[('北京', '北京'), ('上海', '上海'), ('广州', '广州'), ('深圳', '深圳'), ('兰州', '兰州'), ('西安', '西安'), ('重庆', '重庆'), ('成都', '成都')], max_length=16, verbose_name='目标城市')),
                ('min_distance', models.IntegerField(default=1, verbose_name='最小查找范围')),
                ('max_distance', models.IntegerField(default=10, verbose_name='最大查找范围')),
                ('min_dating_age', models.IntegerField(default=18, verbose_name='最小交友年龄')),
                ('max_dating_age', models.IntegerField(default=50, verbose_name='最大交友年龄')),
                ('vibration', models.BooleanField(default=True, verbose_name='开启震动')),
                ('only_matche', models.BooleanField(default=True, verbose_name='不让匹配的人看我的相册')),
                ('auto_play', models.BooleanField(default=True, verbose_name='是否自动播放视频')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(choices=[('北京', '北京'), ('上海', '上海'), ('广州', '广州'), ('深圳', '深圳'), ('兰州', '兰州'), ('西安', '西安'), ('重庆', '重庆'), ('成都', '成都')], max_length=8, verbose_name='常居地'),
        ),
    ]