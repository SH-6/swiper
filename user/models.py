from datetime import datetime

from django.db import models


# Create your models here.
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
