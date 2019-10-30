from common import errors


def need_perm(perm_name):
    '''权限检查'''
    def deco(view_func):
        def warp(request):
            #检查VIP是否已过期
            if request.user.vip_remain_day() <= 0:
                raise errors.VIPExpired
            #检查用户是否觉有该权限
            if request.user.vip.has_perm(perm_name):
                return view_func(request)
            else:
                raise errors.NotHasPerm
        return warp
    return deco