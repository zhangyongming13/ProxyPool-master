import redis, random
from proxypool.error import PoolEmptyError
from proxypool.setting import HOST, PORT, PASSWORD


class RedisClient(object):
    def __init__(self, host=HOST, port=PORT):
        if PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)

    def get(self, count=1):
        """
        get proxies from redis
        """
        proxies = self._db.lrange("proxies", 0, count - 1)
        self._db.ltrim("proxies", count, -1)
        return proxies

    def put(self, proxy):
        """
        add proxy to right top
        """
        # if self._db.sismember("proxies", proxy):
        #     print('该代理已经存在：', proxy)
        # else:
        #     self._db.rpush("proxies", proxy)
        self._db.rpush("proxies", proxy)

    def pop(self):
        """
        get proxy from right.
        """
        # try:
        #     self._db.randomkey()
        #     return self._db.rpop("proxies").decode('utf-8')
        # except:
        #     raise PoolEmptyError
        try:
            db = redis.Redis(host='192.168.1.247', port=6379)
            len = db.llen("proxies")
            zhang = random.randint(0, len)
            proxy = db.lrange("proxies", zhang, zhang)[0].decode('utf-8')
            return proxy
        except Exception as e:
            print(e)
            raise PoolEmptyError

    @property
    def queue_len(self):
        """
        get length from queue.
        """
        return self._db.llen("proxies")

    def flush(self):
        """
        flush db
        """
        self._db.flushall()


if __name__ == '__main__':
    conn = RedisClient()
    print(conn.pop())
