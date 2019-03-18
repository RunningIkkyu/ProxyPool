import sys
import time
import asyncio
try:
    from aiohttp import ClientError 
except:     
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
import aiohttp
from proxypool.db import RedisClient
from proxypool.setting import TEST_URL, BATCH_TEST_SIZE, VALID_STATUS_CODES


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
            "User-Agent": "Mozilla/5.0 (WindowsNT 10.0; WOW64)"\
                          " AppleWebKit/537.36 (KHTML, like Gecko)" \
                          " Chrome/72.0.3626.121 Safari/537.36"   
        }

        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn, headers=headers) as session:
        #async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('Testing proxy: ', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15,
                                       allow_redirects=False) as response:
                    if response.status in  VALID_STATUS_CODES:
                        print('Proxy', proxy, 'test success! ')
                        self.redis.max(proxy)
                    else:
                        print('Proxy', proxy, 'test failed! ')
                        self.redis.decrease(proxy)
                        print('Proxy test failed: ', response.status, ' IP:', proxy)
            except Exception as e:
            #except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print('Proxy connected failed : ', e)

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


