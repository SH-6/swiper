from django.db import models


# Create your models here.

class Swiped(models.Model):
    STYPE = (
        ('superlike', '上滑'),
        ('like', '右滑'),
        ('dislike', '左滑')
    )
    uid = models.IntegerField(verbose_name='滑动者ID')
    sid = models.IntegerField(verbose_name='被滑动者ID')
    stype = models.IntegerField(max_length=16, choices=STYPE, verbose_name='滑动类型')
    stime = models.DateTimeField(verbose_name='滑动时间')
