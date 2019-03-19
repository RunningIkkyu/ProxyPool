import sys
import time
import threading
from queue import Queue
from threading import Lock
import requests
from requests.packages import urllib3
from proxypool.db import RedisClient
from proxypool.setting import TEST_URL, BATCH_TEST_SIZE, VALID_STATUS_CODES


class Tester(object):
    """ Test the availiabilit of proxy. """
    def __init__(self):
        self.redis = RedisClient()
        self.redis.all()
        self.lock = threading.Lock()
        self.mq = Queue()

    def test_proxy(self):
        """ test one proxy. """

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
        headers1 = {
            'Connection': 'close',
        }
        try:
            proxy = self.mq.get()
        except Exception as e:
            print('[ERROR] No proxy to get.')
            return
        real_proxy = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy,
        }
        try:
            urllib3.disable_warnings()
            session = requests.Session()
            requests.adapters.DEFAULT_RETRIES = 5
            session.keep_alive = False
            response = session.get(TEST_URL,  proxies=real_proxy, verify=False, timeout=6,
            headers=headers)
        except Exception as e:
            print("[INFO] Proxy cannot connected: {}. ".format(proxy))
            self.lock.acquire()
            self.redis.decrease(proxy)
            self.lock.release()
            return
        if response.text.find('密码'):
            print("[INFO] Proxy tested success {}.".format(proxy))
            self.lock.acquire()
            self.redis.max(proxy)
            self.lock.release()
        else:
            print('[INFO] Proxy tested failed, status code: {}'.format(proxy,
                                                                          response.status_code))
            self.lock.acquire()
            self.redis.decrease(proxy)
            self.lock.release()


    def run(self):
        print('Proxy tester started.')
        try:
            count = self.redis.count()
            print(count, ' proxies in total.')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print('Testing', start + 1, '-', stop, 'proxy')
                self.mq = self.redis.batch(start, stop)
                thread_list = []
                for _i in range(BATCH_TEST_SIZE):
                    thread = threading.Thread(target=self.test_proxy)
                    thread.start()
                    thread_list.append(thread)
                for _i in range(BATCH_TEST_SIZE):
                    thread_list[_i].join()
                sys.stdout.flush()
                #time.sleep(5)
        except Exception as e:
            print('Tester Error!', e.args)


