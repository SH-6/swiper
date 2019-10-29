from django.db import models
from django.db.models import Q
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

    class Meta:
        ordering = ['stime']

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

    @classmethod
    def who_like_me(cls, uid, num=50):
        swiped_list = cls.objects.filter(sid=uid,
                                         stype__in=['superlike', 'like']
                                         ).order_by('-stime')[:num]
        return swiped_list


class Friend(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def make_friends(cls, uid1, uid2):
        '''建立好友关系'''
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        cls.objects.get_or_create(uid1=uid1, uid2=uid2)
        return True

    @classmethod
    def is_friends(cls, uid1, uid2):
        '''检查两人是否是好友'''
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        return cls.objects.filter(uid1=uid1, uid2=uid2).exists()

    @classmethod
    def break_off(cls, uid1, uid2):
        '''绝交'''
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        cls.objects.filter(uid1=uid1, uid2=uid2).delete()

    @classmethod
    def my_friends(cls, uid):
        '''获取我的好友'''

        query_condition = Q(uid1=uid) | Q(uid2=uid)
        friends = cls.objects.filter(query_condition)
        friend_id_list = []
        for frd in friends:
            friend_id = frd.uid1 if frd.uid1 != uid else frd.uid2
            friend_id_list.append(friend_id)
            return friend_id_list
