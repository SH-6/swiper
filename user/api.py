from django.shortcuts import render
from django.http import JsonResponse
from user.logics import send_vcode


# Create your views here.
def get_vcode(request):
    '''获取验证码接口'''
    phonenum = request.GET.get('phonenum')
    is_success = send_vcode(phonenum)
    return JsonResponse({'code': 0, 'data': is_success})


def submit_vcode(request):
    '''提交验证码,进行登录'''
    pass
    # return JsonResponse()
