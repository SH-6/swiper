#!/d/python3.6.4/python36


import os
import sys
import random
from datetime import date

import django

# 设置环境
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiper.settings")
django.setup()

from user.models import User

last_names = (
    '赵钱孙李周吴郑王冯陈楮卫蒋沈韩杨'
    '朱秦尤许何吕施张孔曹严华金魏陶姜'
    '戚谢邹喻柏水窦章云苏潘葛奚范彭郎'
    '鲁韦昌马苗凤花方俞任袁柳酆鲍史唐'
    '费廉岑薛雷贺倪汤滕殷罗毕郝邬安常'
    '乐于时傅皮卞齐康伍余元卜顾孟平黄'
)
first_names = {
    'male': [
        '致远', '骏驰', '雨泽',
        '天佑', '思聪', '雨辰'

    ],
    'female': [
        '佩玲', '欣妍', '佳琪',
        '雅芙', '雨婷', '雪晴'

    ]
}


def random_name():
    '''随机产生一个名字'''
    last_name = random.choice(last_names)
    sex = random.choice(list(first_names.keys()))
    first_name = random.choice(first_names[sex])
    return ''.join([last_name, first_name]), sex


def create_robots(n):
    # 创建初始用户
    for i in range(n):
        name, sex = random_name()
        try:
            year = random.randint(1970, 2000)
            month = random.randint(1, 12)
            day = random.randint(1, 28)

            User.objects.create(
                phonenum='%s' % random.randrange(21000000000, 21900000000),
                nickname=name,
                sex=sex,
                birth_day=date(year, month, day),
                location=random.choice(['北京', '上海', '广州', '深圳',
                                        '兰州', '西安', '重庆', '成都']),
            )
            print('created:%s %s' % (name, sex))
        except django.db.utils.IntegrityError:
            pass

if __name__ == '__main__':
    create_robots(5000)