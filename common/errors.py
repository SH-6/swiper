'''接口的状态码'''

OK = 0
VCODE_ERR = 1000 #验证码错误
VCODE_EXPIREO = 1001 #验证码过期
WB_AUTH_ERR = 1002 #微博认证错误
LOGIN_REQUIRED = 1003 #需要先登录
PROFILE_ERR = 1004#提交的个人资料有误