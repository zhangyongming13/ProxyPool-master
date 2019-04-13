from bs4 import BeautifulSoup

from .utils import get_page
from pyquery import PyQuery as pq
import re, time, random, requests
# from bs4 import BeautifulSoup
from proxypool.setting import HEADERS, url_ip3366, url_xici


class ProxyMetaclass(type):
    """
        元类，在FreeProxyGetter类中加入
        __CrawlFunc__和__CrawlFuncCount__
        两个参数，分别表示爬虫函数，和爬虫函数的数量。
    """

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(object, metaclass=ProxyMetaclass):
    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):
            print( '爬虫', callback, '获取到', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_ip_ip3366(self):
        number = 1
        # ip_list = []
        while number < 3:
            html = requests.get(url_ip3366.format(str(number)), headers=HEADERS).text
            # print(html.decode(encoding='GB2312'))
            # data = etree.HTML(html)
            # ip_port = data.xpath('//div[@id="footer"]/div[@align="center"]/table/tbody')
            ip_init = re.findall('<td>\d+\.\d+\.\d+\.\d+</td>', html)
            port_init = re.findall('<td>\d*</td>', html)
            proc_init = re.findall('<td>HTTP\w?</td>', html)
            for i in range(len(ip_init)):
                ip_init[i] = re.split('[><]+', ip_init[i])[2]
                port_init[i] = re.split('[<>]+', port_init[i])[2]
                proc_init[i] = re.split('[<>]', proc_init[i])[2]
            for i in range(len(ip_init)):
                # dict = {}
                # dict[proc_init[i]] = ip_init[i] + ':' + port_init[i]
                proxy = '{protocol}'.format(protocol=proc_init[i]) + '://' + '{host}:{port}'.format(host=ip_init[i],
                                                                                   port=port_init[i])
                # pro = re.split(r'[\:\/\/]', proxy)
                # proxy_dict = {pro[0]:pro[3] + ':' + pro[4]}
                yield proxy
                # ip_list.append(dict)
            number = number + 1
            time.sleep(10 + random.randint(20, 100) / 20)

    def crawl_ip_kuaidaili(self):
        # start_time = time.time()
        url_kuaidaili = 'https://www.kuaidaili.com/free/inha/{}/'
        number = 1
        # ip_list = []
        # uncheck_ip_list = []
        while number <= 3:
            try:
                html = requests.get(url_kuaidaili.format(str(number)), headers=HEADERS).text
                ip_init = re.findall('<td data-title="IP">\d+\.\d+\.\d+\.\d+</td>', html)
                port_init = re.findall('<td data-title="PORT">\d*</td>', html)
                proc_init = re.findall('<td data-title="类型">HTTP\w?</td>', html)
                for i in range(len(ip_init)):
                    ip_init[i] = re.split('[><]+', ip_init[i])[2]
                    port_init[i] = re.split('[<>]+', port_init[i])[2]
                    proc_init[i] = re.split('[<>]', proc_init[i])[2]
                for i in range(len(ip_init)):
                    proxy = '{pro_int}://{ip_init}:{port_init}'.format(pro_int=proc_init[i], ip_init=ip_init[i],
                                                                       port_init=port_init[i])
                    # print(proxy)
                    yield proxy
                # proxy = '{pro_int}://{ip_init}:{port_init}'.format(pro_int=proc_init, ip_init=ip_init, port_init=port_init)
                # print(proxy)
                # yield proxy
                # split_built_init_data(ip_init, port_init, proc_init, uncheck_ip_list)
                number = number + 1
                time.sleep(10 + random.randint(20, 100) / 20)
            except Exception:
                print(Exception)
                if number > 1:
                    number = number - 1
                time.sleep(40 + random.randint(20, 100) / 10)
        # threading_for_check_ip(uncheck_ip_list, ip_list)
        # end_time = time.time()
        # print('爬取完毕，整个爬取时间：', end_time - start_time)
        # return ip_list

    def crawl_ip_xici(self):
        number = 1
        while number <= 2:
            html = requests.get(url=url_xici.format(str(number)), headers=HEADERS).content
            soup = BeautifulSoup(html, 'html.parser')
            body = soup.find('table', {'id': 'ip_list'})
            ip_list = body.find_all('tr', {'class': 'odd'})
            for i in ip_list:
                data = i.find_all('td')
                ip = data[1].string
                port = data[2].string
                protocol = data[5].string
                # pro[protocol] = ip + ':' + port
                proxy = '{protocol}'.format(protocol=protocol) + '://' + '{host}:{port}'.format(host=ip, port=port)
                yield proxy
            number += 1
            time.sleep(10 + random.randint(20, 100) / 20)

    # def crawl_kuaidaili(self):
    #     for page in range(1, 4):
    #         # 国内高匿代理
    #         start_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)
    #         html = get_page(start_url)
    #         ip_adress = re.compile(
    #             '<td data-title="IP">(.*)</td>\s*<td data-title="PORT">(\w+)</td>'
    #         )
    #         re_ip_adress = ip_adress.findall(str(html))
    #         for adress, port in re_ip_adress:
    #             result = adress + ':' + port
    #             proxy = result.replace(' ', '')
    #             yield proxy
    #         time.sleep(10 + random.randint(3, 5))
    #
    # def crawl_xicidaili(self):
    #     for page in range(1, 4):
    #         start_url = 'http://www.xicidaili.com/wt/{}'.format(page)
    #         html = get_page(start_url)
    #         ip_adress = re.compile(
    #             '<td class="country"><img src="http://fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>'
    #         )
    #         # \s* 匹配空格，起到换行作用
    #         re_ip_adress = ip_adress.findall(str(html))
    #         for adress, port in re_ip_adress:
    #             result = adress + ':' + port
    #             yield result.replace(' ', '')
    #         time.sleep(10 + random.randint(3, 5))
    #
    # def crawl_daili66(self, page_count=4):
    #     start_url = 'http://www.66ip.cn/{}.html'
    #     urls = [start_url.format(page) for page in range(1, page_count + 1)]
    #     for url in urls:
    #         print('Crawling', url)
    #         html = get_page(url)
    #         if html:
    #             doc = pq(html)
    #             trs = doc('.containerbox table tr:gt(0)').items()
    #             for tr in trs:
    #                 ip = tr.find('td:nth-child(1)').text()
    #                 port = tr.find('td:nth-child(2)').text()
    #                 yield ':'.join([ip, port])
    #         time.sleep(5 + random.randint(1, 3))
    #
    # def crawl_data5u(self):
    #     for i in ['gngn']:
    #         start_url = 'http://www.data5u.com/free/{}/index.shtml'.format(i)
    #         html = get_page(start_url)
    #         ip_adress = re.compile(
    #             ' <ul class="l2">\s*<span><li>(.*?)</li></span>\s*<span style="width: 100px;"><li class=".*">(.*?)</li></span>'
    #         )
    #         # \s * 匹配空格，起到换行作用
    #         re_ip_adress = ip_adress.findall(str(html))
    #         for adress, port in re_ip_adress:
    #             result = adress + ':' + port
    #             yield result.replace(' ', '')
