'''接口的状态码'''

OK = 0


# VCODE_ERR = 1000  # 验证码错误
# VCODE_EXPIREO = 1001  # 验证码过期
# WB_AUTH_ERR = 1002  # 微博认证错误
# LOGIN_REQUIRED = 1003  # 需要先登录
# PROFILE_ERR = 1004  # 提交的个人资料有误


class LogicError(Exception):
    code = None

    def __init__(self, data=None):
        self.data = data or str(self)

    def __str__(self):
        return self.__class__.__name__


def gen_logic_err(name, code):
    attr_dict = {'code': code}
    return type(name, (LogicError,), attr_dict)


VcodeErr = gen_logic_err('VcodeErr', 1000)  # 验证码错误
VcodeExpired = gen_logic_err('VcodeExpired', 1001)  # 验证码过期
WbAuthErr = gen_logic_err('WbAuthErr', 1002)  # 微博认证错误
LoginRequired = gen_logic_err('LoginRequired', 1003)  # 需要先登录
ProfileErr = gen_logic_err('ProfileErr', 1004)  # 提交的个人资料有误
StypeErr = gen_logic_err('StypeErr', 1005)  # 滑动类型错误
NotFoundSwiped = gen_logic_err('NotFoundSwiped', 1006)  #没有找到
LastSwipedTimeout = gen_logic_err('LastSwipedTimeout', 1007)  # 上一次滑动已超时
RewindTimesLimit = gen_logic_err('RewindTimesLimit', 1008)  # 反悔次数达到上限
