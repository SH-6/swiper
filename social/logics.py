from user.models import User
import datetime

def get_rmcd_users(user):
    '''获取推荐用户列表'''
    today = datetime.date.today()
    max_dating_age = today - datetime.date.timedelta(user.profile.min_dating_age * 365)
    min_dating_age = today - datetime.date.timedelta(user.profile.max_dating_age * 365)


    #过滤
    User.objects.filter(
        sex=user.profile.dating_sex,
        location=user.profile.location,
        birth_day__lte=max_birth_date,
        birth_day__gte=min_birth_date,

    )
    return rcmd_user_list
