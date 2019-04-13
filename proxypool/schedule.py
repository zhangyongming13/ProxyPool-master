import time
from multiprocessing import Process
import asyncio, requests,re
import aiohttp
try:
    from aiohttp.errors import ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
from proxypool.db import RedisClient
from proxypool.error import ResourceDepletionError
from proxypool.getter import FreeProxyGetter
from proxypool.setting import *
from asyncio import TimeoutError


class ValidityTester(object):
    test_api = TEST_API

    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []

    def set_raw_proxies(self, proxies):
        self._raw_proxies = proxies
        self._conn = RedisClient()

    # async def test_single_proxy(self, proxy):
    #     """
    #     text one proxy, if valid, put them to usable_proxies.
    #     """
    #     try:
    #         async with aiohttp.ClientSession() as session:
    #             try:
    #                 if isinstance(proxy, bytes):
    #                     proxy = proxy.decode('utf-8')
    #                 print('正在测试:', proxy)
    #                 async with session.get(self.test_api, proxy=proxy, timeout=get_proxy_timeout) as response:
    #                     if response.status == 200:
    #                         self._conn.put(proxy)
    #                         print('可用代理:', proxy)
    #             except Exception as e:
    #                 print(e)
    #                 print('不可用代理:', proxy)
    #     except (ServerDisconnectedError, ClientResponseError,ClientConnectorError) as s:
    #         print(s)
    #         pass

    def test_single_proxy(self, proxy):
        """
        text one proxy, if valid, put them to usable_proxies.
        """
        try:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    # real_proxy = 'http://' + proxy
                    print('正在测试:', proxy)
                    # async with session.get(self.test_api, proxy=real_proxy, timeout=get_proxy_timeout) as response:
                    pro = re.split(r'[\:\/\/]', proxy)
                    proxy_dict = {pro[0]: pro[3] + ':' + pro[4]}
                    response = requests.get(url=TEST_API, proxies=proxy_dict, timeout=5)
                    if response.status_code == 200:
                        self._conn.put(proxy)
                        print('可用代理:', proxy)
                except Exception as e:
                    print(e)
                    print('不可用代理:', proxy)
        except (ServerDisconnectedError, ClientResponseError,ClientConnectorError) as s:
            print(s)
            pass

    def test(self):
        """
        aio test all proxies.
        """
        print('进行代理可用性测试:')
        try:
            # loop = asyncio.get_event_loop()
            # tasks = [self.test_single_proxy(proxy) for proxy in self._raw_proxies]
            # loop.run_until_complete(asyncio.wait(tasks))
            for proxy in self._raw_proxies:
                self.test_single_proxy(proxy)
        except Exception as e:
            print(e)
            print('Async Error!')


class PoolAdder(object):
    """
    add proxy to pool
    """

    def __init__(self, threshold):
        self._threshold = threshold
        self._conn = RedisClient()
        self._tester = ValidityTester()
        self._crawler = FreeProxyGetter()

    def is_over_threshold(self):
        """
        judge if count is overflow.
        """
        if self._conn.queue_len >= self._threshold:
            return True
        else:
            return False

    def add_to_queue(self):
        print('添加代理进行中：')
        proxy_count = 0
        while not self.is_over_threshold():
            for callback_label in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[callback_label]
                raw_proxies = self._crawler.get_raw_proxies(callback)
                # test crawled proxies
                self._tester.set_raw_proxies(raw_proxies)
                self._tester.test()
                proxy_count += len(raw_proxies)
                if self.is_over_threshold():
                    print('代理数量足够！')
                    break
            if proxy_count == 0:
                raise ResourceDepletionError


class Schedule(object):
    @staticmethod
    def valid_proxy(cycle=VALID_CHECK_CYCLE):
        """
        获取队列中一半的代理进行可用性测试！
        """
        conn = RedisClient()
        tester = ValidityTester()
        while True:
            print('测试redis队列代理可用性：')
            count = int(0.5 * conn.queue_len)
            if count == 0:
                print('代理池为空或者全部测试完毕！')
                time.sleep(cycle)
                continue
            raw_proxies = conn.get(count)
            tester.set_raw_proxies(raw_proxies)
            tester.test()
            time.sleep(cycle)

    @staticmethod
    def check_pool(lower_threshold=POOL_LOWER_THRESHOLD,
                   upper_threshold=POOL_UPPER_THRESHOLD,
                   cycle=POOL_LEN_CHECK_CYCLE):
        """
        If the number of proxies less than lower_threshold, add proxy
        """
        conn = RedisClient()
        adder = PoolAdder(upper_threshold)
        while True:
            if conn.queue_len < lower_threshold:
                # 代理数量少于下限进行添加代理操作
                print('Check Pool程序检测到代理数量低于最小值，进行代理补充！')
                adder.add_to_queue()
            time.sleep(cycle)

    def run(self):
        print('IP 地址池正在运行！')
        valid_process = Process(target=Schedule.valid_proxy)
        check_process = Process(target=Schedule.check_pool)
        valid_process.start()
        check_process.start()
