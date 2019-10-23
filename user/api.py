from urllib.parse import urlencode

from django.shortcuts import redirect
from django.core.cache import cache
from django.http import JsonResponse

from swiper import config as cfg
from common import keys
from common import errors

from user import logics
from user.models import User


# Create your views here.
def get_vcode(request):
    '''获取验证码接口'''
    phonenum = request.GET.get('phonenum')
    is_success = logics.send_vcode(phonenum)
    return JsonResponse({'code': 0, 'data': is_success})


def submit_vcode(request):
    '''提交验证码,进行登录'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    # 从缓存中取出用户的验证码
    cached_vcoed = cache.get(keys.VCODE_KEY % phonenum)

    # 检查验证码是否过期
    if cached_vcoed == None:
        return JsonResponse({'code': errors.VCODE_EXPIREO, 'data': None})

    if cached_vcoed == vcode:
        # 先取出用户,如果存在直接取出,如果不存在直接创建
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)

        # 执行登录流程
        request.session['uid'] = user.id
        return JsonResponse({'code': 0, 'data': user.to_dict()})
    else:
        return JsonResponse({'code': errors.VCODE_ERR, 'data': None})


def weibo_authorize(request):
    '''引导用户到授权页面'''
    params = urlencode(cfg.WB_AUTH_PARAMS)
    wb_auth_url = '%s?%s' % (cfg.WB_AUTH_API, params)
    return redirect(wb_auth_url)


def wb_callback(request):
    '''微博回调接口'''
    code = request.GET.get('code')
    access_token, wb_uid = logics.get_access_token(code)

    # 检查 token是否有效
    if access_token is None:
        return JsonResponse({'code': errors.WB_AUTH_ERR, 'data': None})

    # 获取微博用户数据
    user_info = logics.get_wb_user_info(access_token, wb_uid)

    # 执行登良注册流程
    try:
        user = User.objects.get(phonenum=user_info['phonenum'])
    except User.DoesNotExist:
        user = User.objects.create(**user_info)

    # 执行登录流程
    request.session['uid'] = user.id
    return JsonResponse({'code': 0, 'data': user.to_dict()})
