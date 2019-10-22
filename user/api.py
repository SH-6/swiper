from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse

from common import keys
from common import errors

from user.logics import send_vcode
from user.models import User


# Create your views here.
def get_vcode(request):
    '''获取验证码接口'''
    phonenum = request.GET.get('phonenum')
    is_success = send_vcode(phonenum)
    return JsonResponse({'code': 0, 'data': is_success})


def submit_vcode(request):
    '''提交验证码,进行登录'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    # 从缓存中取出用户的验证码
    cached_vcoed = cache.get(keys.VCODE_KEY % phonenum)

    if cached_vcoed == vcode:
        # 先取出用户,如果存在直接取出,如果不存在直接创建
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)

        # 执行登录流程
        request.session['uid'] = user.id
        return JsonResponse({'code': 0,'data': user.to_dict()})
    else:
        return JsonResponse({'code': errors.VCODE_ERR, 'data': None})
