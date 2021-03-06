from proxypool.tester import Tester
from proxypool.db import RedisClient
from proxypool.crawler import Crawler
from proxypool.setting import POOL_UPPER_THRESHOLD, PRIVATE_PROXY_ENABLE
from proxypool.private_proxy import PrivateProxy
import sys

class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()
    
    def is_over_threshold(self):
        """ Check if the mount of proxies is over threshold."""
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
    
    def run(self):
        print('Getter started.')
        if PRIVATE_PROXY_ENABLE:
            proxies = PrivateProxy().get_proxies()
            for proxy in proxies:
                print('Add private proxy {}'.format(proxy))
                self.redis.add(proxy)
        else:
            if not self.is_over_threshold():
                for callback_label in range(self.crawler.__CrawlFuncCount__):
                    callback = self.crawler.__CrawlFunc__[callback_label]
                    # 获取代理
                    proxies = self.crawler.get_proxies(callback)
                    sys.stdout.flush()
                    for proxy in proxies:
                        self.redis.add(proxy)
