import logging

from urllib.parse import urlencode

from django.shortcuts import redirect
from django.core.cache import cache

from libs.http import render_json
from swiper import config as cfg
from common import keys
from common import errors

from user import logics
from user.models import User
from user.forms import ProfileForm

info_log = logging.getLogger('inf')


def get_vcode(request):
    '''获取验证码接口'''
    phonenum = request.GET.get('phonenum')
    is_success = logics.send_vcode(phonenum)
    return render_json(is_success)


def submit_vcode(request):
    '''提交验证码,进行登录'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    # 从缓存中取出用户的验证码
    cached_vcoed = cache.get(keys.VCODE_KEY % phonenum)

    # 检查验证码是否过期
    if cached_vcoed == None:
        return errors.VcodeExpired
    if cached_vcoed == vcode:
        # 先取出用户,如果存在直接取出,如果不存在直接创建
        try:
            user = User.objects.get(phonenum=phonenum)
            info_log.info(f'login:{user.id}')
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)
            info_log.info(f'register:{user.id}')

        # 执行登录流程
        request.session['uid'] = user.id
        return render_json(user.to_dict())
    else:
        return errors.VcodeErr


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
        return errors.WbAuthErr

    # 获取微博用户数据
    user_info = logics.get_wb_user_info(access_token, wb_uid)

    # 执行登良注册流程
    try:
        user = User.objects.get(phonenum=user_info['phonenum'])
    except User.DoesNotExist:
        user = User.objects.create(**user_info)

    # 执行登录流程
    request.session['uid'] = user.id
    return render_json(user.to_dict())


def get_profile(request):
    '''获取个人资料'''
    key = keys.PROFILE_KEY % request.user.id
    profile_data = cache.get(key)
    info_log.debug(f'从缓存取数据:{profile_data}')
    if profile_data is None:
        profile_data = request.user.profile.to_dict()
        info_log.debug(f'从数据库取数据{profile_data}')
        cache.set(key, profile_data)  # 将数据添加到缓存
        info_log.debug(f'将数据添加到缓存')
    return render_json(profile_data)


def set_profile(request):
    '''修改个人资料'''
    form = ProfileForm(request.POST)
    # 数据检查
    if form.is_valid():
        profile = form.save(commit=False)  # 通过Form表单创建出model对象,但并不在数据库中创建
        profile.id = request.user.id  # 给profile设置id
        profile.save()  # 保存
        info_log.debug('更新缓存')
        return render_json(profile.to_dict())
    else:
        raise errors.ProfileErr(form.errors)


def upload_avatar(request):
    '''上传个人资料'''
    avatar = request.FILES.get('avatar')
    logics.upload_avatar.delay(request.user, avatar)
    return render_json()
