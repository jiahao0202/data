from patterns.singleton import Singleton
from redis import Redis
from redis_config import *


class RedisHelper(metaclass=Singleton):
    def __init__(self):
        self.__conn = Redis(
            host=RedisConfig.host,
            port=RedisConfig.port,
            db=RedisConfig.db,
            ssl=True
        )

    def redis_get(self, key):
        return self.__conn.get(key)

    def redis_set(self, key, value):
        return self.__conn.set(key, value)
