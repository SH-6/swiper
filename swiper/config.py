'''程序逻辑及第三方平台的配置'''

# 返回配置
DAILY_REWIND_TIMES = 3
LAST_SWIPED_SECONDS = 300

# 滑动积分配置
# DISLIKE_SCORE = -5
# LIKE_SCORE = 5
# SUPERLIKE_SCORE = 7
SWIPE_SCORE = {
    'like': 5,
    'superlike': 7,
    'dislike': -5
}

# 云之讯短信平台配置
YZX_API = 'https://open.ucpaas.com/ol/sms/sendsms'
YZX_PARAMS = {
    "sid": "a2aa797456427cdd4d936dab15934213",
    "token": "5cffb2bb0f244973299ac0effe15d907",
    "appid": "3a39b0f0c23442d1b4ed891012581cee",
    "templateid": "511342",
    "param": None,
    "mobile": None,
    'uid': None
}

# 微博接入
WB_APP_KEY = '3298304421'
WB_APP_SECRET = 'f462ba9ee44a89ab2f0a423eae18bbb5'
WB_CALLBACK = 'http://127.0.0.1:8000/api/user/weibo/callback'

# 认证API
WB_AUTH_API = 'https://api.weibo.com/oauth2/authorize'
WB_AUTH_PARAMS = {
    'client_id': WB_APP_KEY,
    'redirect_uri': WB_CALLBACK,
    'display': 'default'
}

# 第二步,获取AccessToken
WB_ACCESS_TOKEN_API = 'https://api.weibo.com/oauth2/access_token'
WB_ACCESS_TOKEN_PARAMS = {
    'client_id': WB_APP_KEY,
    'client_secret': WB_APP_SECRET,
    'grant_type': 'authorization_code',
    'redirect_uri': WB_CALLBACK,
    'code': None,
}

# 第三步:获取用户数据
WB_USER_SHOW_API = 'https://api.weibo.com/2/users/show.json'
WB_USER_SHOW_PARAMS = {
    'access_token': None,
    'uid': None
}

# 七牛云配置
QN_ACCESS_KEY = 'dUwTDiMpmk2FFgTS232iGz--wJQ4HZRPAceZ8nYJ'
QN_SECRET_KEY = 'D6hhvBhQDIPy0hlB7R4jSTowtSeW_AW0-9zZZ_AL'
QN_BUCKET = 'zz0000'
QN_BASE_URL = 'http://prl9noner.bkt.clouddn.com'
