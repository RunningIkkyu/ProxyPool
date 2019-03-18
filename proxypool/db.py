import re
import redis
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from proxypool.setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from proxypool.error import PoolEmptyError
#from setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
#from setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
#from error import PoolEmptyError
from random import choice


class RedisClient(object):
    """ A redis client provided db operation."""
    def __init__(self, 
                 host=REDIS_HOST, 
                 port=REDIS_PORT, 
                 password=REDIS_PASSWORD):
        """
        :param host: host of redis.
        :param port: port of redis.
        :param password: password of redis.
        """
        self.db = redis.Redis(host=host, port=port, password=password, decode_responses=True)

    def getscore(self, proxy):
        return self.db.zscore(REDIS_KEY, proxy)


    def add(self, proxy, score=INITIAL_SCORE):
        """
        Add proxy to redis database.
        :param proxy: proxy to add
        :param score: score of proxy
        :return 
        """
        if not re.match(r'\d+\.\d+\.\d+\.\d+:\d+', proxy):
            print('Format problem : ', proxy, '---->Discard')
            return None

        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def greatcount(self):
        return len(self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE))

    def random(self):
        """ Get proxy randomly. """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 10)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        Decrase the score of proxy.  Remove proxy if it's score lower than MIN_SCORE.
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        print("[DEBUG: db.decrease] score = ", score)
        if score and score > MIN_SCORE:
            self.db.zincrby(REDIS_KEY, -1, proxy)
            print('[DEBUG: db.decrease] Proxy: ', proxy, '\t current score:', self.getscore(proxy))
        else:
            print('Proxy: ', proxy, '\t current score:', score, '---> Removed')
            self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """ Check if a proxy exists."""
        return self.db.zscore(REDIS_KEY, proxy) is not None

    def max(self, proxy):
        """ Set the score of a proxy to max."""
        print('Proxy setted to max: ', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):
        """ Return the number of elements in the set."""
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """ Return all proxy in the set """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        return self.db.zrevrange(REDIS_KEY, start, stop-1)


if __name__ == '__main__':
    db = RedisClient()
    proxy = db.random()
    print(db.getscore(proxy))
    db.decrease(proxy)
    print(db.getscore(proxy))
    db.max(proxy)
    print(db.getscore(proxy))


