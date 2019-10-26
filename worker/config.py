# celery 配置

broker_url = 'redis://127.0.0.1:6379/9'
broker_pool_limit = 50 #Borker 连接池,默认是10

timezone = 'Asia/Shanghai'
accept_content = ['pickle', 'json']

task_serializer = 'pickle'
result_expires = 3600 #任务过期时间

result_backecd = 'redis://127.0.0.1:6379/9'
result_serializer = 'pickle'
result_cache_max = 100  # 任务结果最大缓存数量

worker_redirect_stdouts_level = 'INFO'
