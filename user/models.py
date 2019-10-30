from datetime import date, datetime

from django.db import models
from vip.models import Vip


class User(models.Model):
    SEX = (
        ('male', '男性'),
        ('male', '女性')
    )
    LOCTION = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('广州', '广州'),
        ('深圳', '深圳'),
        ('兰州', '兰州'),
        ('西安', '西安'),
        ('重庆', '重庆'),
        ('成都', '成都')
    )
    phonenum = models.CharField(max_length=16, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    sex = models.CharField(max_length=8, choices=SEX, verbose_name='性别')
    birth_day = models.DateTimeField(default=datetime(2000, 1, 1), verbose_name='出生日')
    avatar = models.CharField(max_length=256, verbose_name='个人形象')
    location = models.CharField(max_length=8, choices=LOCTION, verbose_name='常居地')

    # 用户会员记录
    vip_id = models.IntegerField(default=1, verbose_name='VIP 的 ID')
    vip_end_date = models.DateField(default=date(1970, 1, 1), verbose_name='会员结束时间')

    @property
    def profile(self):
        '''获取我的个人资料'''
        if not hasattr(self, '_profile'):  # 检查是否创建过_profile
            # 动态为self添加 profile属性
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    @property
    def vip(self):
        '''用户对应的 VIP'''
        if not hasattr(self, '_vip'):  # 检查是否创建过_vip
            # 动态为self添加 _vip属性
            self._vip, _ = Vip.objects.get(id=self.id)
        return self._vip

    def vip_remain_day(self):
        '''VIP剩余天数'''
        data_delta = self.vip_end_date - date.today()
        if data_delta.days <= 0:
            return 0
        else:
            return data_delta.days

    def to_dict(self):
        return {
            'id': self.id,
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'sex': self.sex,
            'birth_day': str(self.birth_day),
            'avatar': self.avatar,
            'location': self.location,
        }


class Profile(models.Model):
    '''用户资料'''
    SEX = (
        ('male', '男性'),
        ('female', '女性')
    )
    LOCTION = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('广州', '广州'),
        ('深圳', '深圳'),
        ('兰州', '兰州'),
        ('西安', '西安'),
        ('重庆', '重庆'),
        ('成都', '成都')
    )
    # 交友配置
    dating_sex = models.CharField(max_length=16, choices=SEX, verbose_name='匹配的性别')
    location = models.CharField(max_length=16, choices=LOCTION, verbose_name='目标城市')
    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')
    # 客户端配置
    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matche = models.BooleanField(default=True, verbose_name='不让匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='是否自动播放视频')

    def to_dict(self):
        return {
            'dating_sex': self.dating_sex,
            'location': self.location,
            'min_distance': self.min_distance,
            'max_distance': self.max_distance,
            'min_dating_age': str(self.min_dating_age),
            'max_dating_age': self.max_dating_age,
            'vibration': self.vibration,
            'only_matche': self.only_matche,
            'auto_play': self.auto_play,
        }
