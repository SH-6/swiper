from django.utils.deprecation import MiddlewareMixin

from common import errors
from user.models import User
from libs.http import render_json


class UserAuthMiddleware(MiddlewareMixin):
    URL_WHITE_LIST = [
        'api/user/get_vcode',
        'api/user/submit_vcode',
        'api/user/weibo/auth',
        'api/user/weibo/callback'
    ]

    def process_request(self, request):
        # 检查当前URL是否在白名单中,如果在,直接返回
        if request.path in self.URL_WHITE_LIST:
            return

        #通过session检测用户登录状态
        uid = request.session.get('uid')
        if uid is None:
            # 如果用户未登录
            return render_json(code=errors.LOGIN_REQUIRED)
        else:
            #动态为request添加user属性
            request.user = User.objects.get(id=uid)
