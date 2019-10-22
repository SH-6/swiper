import requests
import random
from swiper import config as cfg


def generate_random_number(length=6):
    '''产生一个指定长度的随机数'''
    value = random.randrange(1, 10 ** length)
    template = '%0{}d'.format(length)
    return template % value


def send_vcode(phonenum):
    '''发送验证码'''
    # 生成一个验证码
    vcode = generate_random_number()
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
