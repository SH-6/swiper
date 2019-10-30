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
from vip.models import Permission
from vip.models import Vip
from vip.models import VipPermRelation

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


def init_permission():
    permissions = (
        ('vipflag', '会员身份标识'),
        ('superlike', '超级喜欢'),
        ('rewind', '反悔功能'),
        ('anylocation', '任意更改定位'),
        ('unlimit_like', '无限喜欢次数'),
        ('show_liked_me', '查看喜欢过我的人')
    )

    for name, desc in permissions:
        perm, _ = Permission.objects.get_or_create(name=name, desc=desc)

        print('create permission %s' % perm.name)


def init_vip():
    for i in range(4):
        vip, _ = Vip.objects.get_or_create(
            name='%d 级会员' % i,
            level=i,
        )
        print('create %s' % vip.name)


def create_vip_perm_relations():
    '''创建 Vip 和 Permission 的关系'''
    # 获取 VIP
    vip1 = Vip.objects.get(level=1)
    vip2 = Vip.objects.get(level=2)
    vip3 = Vip.objects.get(level=3)

    # 获取权限
    vipflag = Permission.objects.get(name='vipflag')
    superlike = Permission.objects.get(name='superlike')
    rewind = Permission.objects.get(name='rewind')
    anylocation = Permission.objects.get(name='anylocation')
    unlimit_like = Permission.objects.get(name='unlimit_like')
    show_liked_me = Permission.objects.get(name='show_liked_me')

    # 给 VIP 1分配权限
    VipPermRelation.objects.get_or_create(vip_id=vip1.id, perm_id=vipflag.id)
    VipPermRelation.objects.get_or_create(vip_id=vip1.id, perm_id=superlike.id)

    # 给 VIP 2分配权限
    VipPermRelation.objects.get_or_create(vip_id=vip2.id, perm_id=vipflag.id)
    VipPermRelation.objects.get_or_create(vip_id=vip2.id, perm_id=superlike.id)
    VipPermRelation.objects.get_or_create(vip_id=vip2.id, perm_id=rewind.id)

    # 给 VIP 3分配权限
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=vipflag.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=superlike.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=rewind.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=anylocation.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=unlimit_like.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=show_liked_me.id)


if __name__ == '__main__':
    # create_robots(5000)
    init_permission()
    init_vip()
    create_vip_perm_relations()
