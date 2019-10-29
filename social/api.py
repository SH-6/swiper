from django.shortcuts import render

from libs.http import render_json
from social import logics
from social.models import Swiped
from social.models import Friend
from user.models import User


# Create your views here.

def rcmd_users(request):
    '''获取推荐用户'''
    rcmd_user_list = logics.get_rmcd_users(request.user)
    result = [user.to_dict() for user in rcmd_user_list]
    return render_json(result)


def like(request):
    '''喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.like_someone(request.user, sid)
    return render_json({'is_matched': is_matched})


def superlike(request):
    '''超级喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.superlike_someone(request.user, sid)
    return render_json({'is_matched': is_matched})


def dislike(request):
    '''不喜欢'''
    sid = int(request.POST.get('sid'))
    Swiped.swipe(request.user.id, sid, 'dislike')
    return render_json()


def rewind(request):
    '''反悔'''
    logics.rewind_last_swiped(request.user)
    return render_json()


def show_liked_me(request):
    users_info = logics.who_like_me(request.user)
    return render_json()


def friends(request):
    '''查看我的好友'''
    friend_id_list = Friend.my_friends(request.user.id)
    all_my_friends = User.objects.filter(id__in=friend_id_list)
    friends_info = [frd.to_dict() for frd in all_my_friends]
    return render_json(friends_info)
