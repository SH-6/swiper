from django.shortcuts import render

from libs.http import render_json
from social import logics


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
    return


def rewind(request):
    return


def show_liked_me(request):
    return


def friends(request):
    return
