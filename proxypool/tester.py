import sys
import time
import asyncio
import aiohttp
#from proxypool.db import RedisClient
#from proxypool.setting import TEST_URL
from db import RedisClient
from setting import TEST_URL


class Tester(object):
    """ Test the availiabilit of proxy. """
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """ Asynchronious function to test one proxy. """
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;"\
                          "q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",     
                "Accept-Language": "zh-CN,zh;q=0.9",     
                "Host": "httpbin.org",
                "Upgrade-Insecure-Requests": "1",     
                "User-Agent": "Mozilla/5.0 (WindowsNT 10.0; WOW64) "\
                              "AppleWebKit/537.36 (KHTML, like Gecko) " \
                              "Chrome/72.0.3626.121 Safari/537.36"   
            }

        async with aiohttp.ClientSession(headers=headers) as session:
            real_proxy = 'http://' + proxy
            print('Testing proxy: ', proxy)
            try:
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15,
                                       allow_redirects=False) as response:
                    if response.status == 200:
                        self.redis.max(proxy)
                        print('Proxy test success: ', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('Proxy test failed: ', proxy)
            except Exception as e:
                self.redis.decrease(proxy)
                print('Proxy connect failed: ', proxy)

    def run(self):
        print('Proxy tester started.')
        try:
            count = self.redis.count()
            print(count, ' proxies in total.')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print('Testing', start + 1, '-', stop, 'proxy')
                test_proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print('Tester Error!', e.args)


