import os
import random

import requests
from django.core.cache import cache
from django.conf import settings

from swiper import config as cfg
from libs.qn_cloud import upload_to_qn
from worker import celery_app
from common import keys


def generate_random_number(length=6):
    '''产生一个指定长度的随机数'''
    value = random.randrange(1, 10 ** length)
    template = '%0{}d'.format(length)
    return template % value


def send_vcode(phonenum):
    '''发送验证码'''
    # 生成一个验证码
    vcode = generate_random_number()
    cache.set(keys.VCODE_KEY % phonenum, vcode, 180)  # 将vcoe写入缓存180s后过期
    print('vcode: %s' % vcode)
    # 整理参数
    params = cfg.YZX_PARAMS.copy()
    params['param'] = vcode
    params['mobile'] = phonenum

    # 调用第三方平台的接口,发送验证码
    resp = requests.post(cfg.YZX_API, json=params)
    if resp.status_code == 200:
        result = resp.json()
        print(result)
        if result.get('msg') == 'OK':
            return True
    return False


def get_access_token(auth_code):
    '''获取微博的access_token'''
    # 拼接参数
    params = cfg.WB_ACCESS_TOKEN_PARAMS.copy()
    params['code'] = auth_code

    # 向微博发送请求,获取access token
    resp = requests.post(cfg.WB_ACCESS_TOKEN_API, data=params)
    result = resp.json()

    access_token = result.get('access_token')
    wb_uid = result.get('uid')
    return access_token, wb_uid


def get_wb_user_info(access_token, wb_uid):
    '''获取微博用户的信息'''
    params = cfg.WB_USER_SHOW_PARAMS.copy()
    params['access_token'] = access_token
    params['uid'] = wb_uid

    # 发送请求
    resp = requests.get(cfg.WB_USER_SHOW_API, params=params)
    result = resp.json()

    nickname = result.get('screen_name')
    gender = result.get('gender')  # 性别，m：男、f：女、n：未知
    location = result.get('location')
    avatar = result.get('avatar_hd')

    sex = {'m': 'male', 'f': 'female', 'n': ''}[gender]
    location = location.split()[0]
    phonenum = 'wb_%s' % wb_uid

    return {
        'phonenum': phonenum,
        'nickname': nickname,
        'sex': sex,
        'location': location,
        'avatar': avatar
    }


def save_avatar(uid, upload_file):
    '''将上传的文件保存到硬盘上'''
    filename = 'avatar-%s' % uid
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    with open(filepath, 'wb') as new_file:
        for chunk in upload_file.chunks():
            new_file.write(chunk)
    return filepath, filename


@celery_app.task
def upload_avatar(user, upload_file):
    '''保存用户头像'''
    # 将文件保存到本地
    filepath, filename = save_avatar(user.id, upload_file)
    # 将文件上传到七牛云
    file_url = upload_to_qn(filepath, filename)
    # 保存文件链接
    user.avatar = file_url
    user.save()

    # 删除本地文件
    os.system('rm -f %s' % filepath)
