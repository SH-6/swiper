from pickle import dumps, loads, HIGHEST_PROTOCOL

from redis import Redis as _Redis
from swiper.settings import REDIS


class Redis(_Redis):
    '''對原 Redis 類進行封裝,增加 pickle 支持'''

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        data = dumps(value, HIGHEST_PROTOCOL)
        return super().set(name, data, ex, px, nx, xx)

    def get(self, name):
        data = super().get(name)
        try:
            return loads(data)
        except TypeError:
            return data


rds = Redis(**REDIS)
