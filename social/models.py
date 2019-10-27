from django.db import models

from common import errors


# Create your models here.

class Swiped(models.Model):
    STYPE = (
        ('superlike', '上滑'),
        ('like', '右滑'),
        ('dislike', '左滑')
    )
    uid = models.IntegerField(verbose_name='滑动者ID')
    sid = models.IntegerField(verbose_name='被滑动者ID')
    stype = models.CharField(max_length=16, choices=STYPE, verbose_name='滑动类型')
    stime = models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')

    @classmethod
    def swipe(cls, uid, sid, stype):
        '''滑动操作'''
        # 检测滑动类型是否正确
        if stype not in ['superlike', 'like', 'dislike']:
            raise errors.StypeErr

        # 记录滑动操作
        cls.objects.filter(uid=uid, sid=sid).exists()
        cls.objects.create(uid=uid, sid=sid, stype=stype)

    @classmethod
    def is_like_me(cls, uid, sid):
        cls.objects.filter(uid=uid,
                           sid=sid,
                           stype__in=['superlike', 'like']).exists()


class Friend(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def make_friends(cls, uid1, uid2):
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        cls.objects.get_or_create(uid1=uid1, uid2=uid2)
        return True
