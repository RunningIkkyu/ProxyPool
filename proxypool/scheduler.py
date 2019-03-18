import time
from multiprocessing import Process
from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.db import RedisClient
from proxypool.setting import *


class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """ Tester every cycle."""
        tester = Tester()
        while True:
            print('Tester started.')
            tester.run()
            time.sleep(cycle)
    
    def schedule_getter(self, cycle=GETTER_CYCLE):
        """ Get proxy each cycle."""
        getter = Getter()
        while True:
            print('Getting proxies.')
            getter.run()
            time.sleep(cycle)
    
    def schedule_api(self):
        """ Open API """
        app.run(API_HOST, API_PORT)
    
    def run(self):
        print('Proxy pool is running.')
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
