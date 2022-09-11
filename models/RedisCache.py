import json
import hashlib
from redis import Redis

red4 = Redis(host='localhost', port=6379, db=4)


class RedisCache(object):
    time_expired = 60 * 60 * 24 * 30
    prefix_key = ''

    def __create_key__(self, data):
        dictn_hex = hashlib.sha256(data).hexdigest()
        return self.prefix_key + dictn_hex

    def set(self, dictn):
        data = json.dumps(dictn).encode('utf-8')
        key = self.__create_key__(data)
        red4.set(key, data)
        red4.expire(key, self.time_expired)

    def keys_iterator(self):
        return red4.scan_iter(self.prefix_key + '*', count=1)

    @staticmethod
    def pop(key):
        pop_ = RedisCache.get(key)
        red4.delete(key)

        return pop_

    @staticmethod
    def get(key):
        return red4.get(key)

    @staticmethod
    def db_size():
        return red4.dbsize()
