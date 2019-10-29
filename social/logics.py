import datetime

from django.core.cache import cache
from swiper import config as cfg
from common import keys
from user.models import User
from social.models import Swiped
from social.models import Friend
from common import errors


def get_rmcd_users(user):
    '''获取推荐用户列表'''
    # 计算出生日期范围
    today = datetime.date.today()
    max_birth_date = today - datetime.timedelta(user.profile.min_dating_age * 365)
    min_birth_date = today - datetime.timedelta(user.profile.max_dating_age * 365)

    # 取出自身滑动过的用户的 id
    sid_list = Swiped.objects.filter(uid=user.id).values_list('sid', flat=True)

    # 过滤
    rcmd_user_list = User.objects.filter(
        sex=user.profile.dating_sex,
        location=user.profile.location,
        birth_day__lte=max_birth_date,
        birth_day__gte=min_birth_date,
    ).exclude(id__in=sid_list)[:20]
    return rcmd_user_list


def like_someone(user, sid):
    '''喜欢了某人'''
    Swiped.swipe(user.id, sid, 'like')  # 添加了滑动记录

    # 检查是否互相喜欢过
    if Swiped.is_like_me(user.id, sid):
        Friend.make_friends(user.id, sid)  # 创建好友关系
        return True
    else:
        return False


def superlike_someone(user, sid):
    '''超级喜欢了某人'''
    Swiped.swipe(user.id, sid, 'like')  # 添加了滑动记录

    # 检查是否互相喜欢过
    if Swiped.is_like_me(user.id, sid):
        Friend.make_friends(user.id, sid)  # 创建好友关系
        return True
    else:
        return False


def rewind_last_swiped(user):
    '''反悔上一次滑动'''
    # 查找上一次操作
    last_swiped = Swiped.objects.filter(uid=user.id).last()
    if last_swiped is None:
        # 如果用户没有任何操作记录,直接返回
        raise errors.NotFoundSwiped

    # 检查反悔的记录是否是五分钟之内的
    time_zone = last_swiped.stime.tzinfo
    now = datetime.datetime.now(tz=time_zone)
    if (now - last_swiped.stime).seconds > cfg.LAST_SWIPED_SECONDS:
        raise errors.LastSwipedTimeout

    # 检查是否达到当天反悔次数上限
    rewind_key = keys.REWIND_TIMES % (user.id, now.date())
    current_rewind_times = cache.get(rewind_key, 0)  # 当天反悔次数
    if current_rewind_times >= 3:
        raise errors.RewindTimesLimit

    # 计算当前时刻到凌晨零点的剩余秒数
    year, month, day, *_ = now.timetuple()  # 取出今天的年,月,日
    remain_time = datetime.datetime(year, month, day + 1, tzinfo=time_zone) - now  # 计算剩余时间

    # 更新缓存
    current_rewind_times += 1
    cache.set(rewind_key, current_rewind_times, remain_time.total_seconds())

    # 如何记录反悔次数
    # 每天凌晨如何清零

    # 喜欢类型的撤销操作,需要先检查是否匹配过好友
    if last_swiped.stype in ['like', 'superlike']:
        # 如果是好友,撤销好友关系
        Friend.break_off(user.id, last_swiped.sid)
    # 删除
    last_swiped.delete()


def who_like_me(user):
    # 取出滑动记录
    swiped_list = Swiped.who_like_me(user.id)

    # 取出对面的user
    uid_list = [swp.uid for swp in swiped_list]
    users = User.objects.in_bulk(uid_list)

    # 封装返回值
    users_info = []
    for swp in swiped_list:
        user = users[swp.uid]
        info = user.to_dict()
        info['stype'] = swp.stype
        info['stime'] = str(swp.stime)
        users_info.append(info)
        return users_info
