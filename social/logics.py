import datetime

from user.models import User
from social.models import Swiped


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


def like_someone(user,sid):
    '''喜欢了某人'''
    Swiped.objects.create('')

def superlike_someone(user,sid):
    '''超级喜欢了某人'''

