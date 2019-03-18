import re
import json
import sys
import requests
from lxml.etree import HTML
import lxml
#from util.UtilFunctions import getHtmlTree


class GetProxy(object):
    @staticmethod
    def getProxy_one(page_count=1):
        """
        西刺代理 http://www.xicidaili.com
        :return:
        """
        url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        for each_url in url_list:
            for i in range(1, page_count + 1):
                page_url = each_url + str(i)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ':'.join(proxy.xpath('./td/text()')[0:2])
                    except Exception as e:
                        pass

    @staticmethod
    def getProxy_two():
        """
        快代理 https://www.kuaidaili.com
        """
        url_list = [
            'https://www.kuaidaili.com/free/inha/',
            'https://www.kuaidaili.com/free/intr/'
        ]
        for url in url_list:
            tree = getHtmlTree(url)
            proxy_list = tree.xpath('.//table//tr')
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def getProxy_three():
        """
        云代理 http://www.ip3366.net/free/
        :return:
        """
        urls = ['http://www.ip3366.net/free/']
        #request = WebRequest()
        for url in urls:
            r = requests.get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def getProxy_four():
        """
        IP海 http://www.iphai.com/free/ng
        :return:
        """
        urls = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp'
        ]
        #request = WebRequest()
        for url in urls:
            r = requests.get(url, timeout=10)
            proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                 r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def getProxy_five():
        '''
        方法CEO
        https://ip.seofangfa.com/
        '''
        url = 'https://ip.seofangfa.com/'
        r = requests.get(url)
        html = HTML(r.text)
        tbody = html.xpath('//table[@class="table"]/tbody')[0]
        for tr in tbody:
            yield tr[0].text + ':' + tr[1].text

    @staticmethod
    def getProxy_six():
        '''
        开心代理
        http://ip.kxdaili.com/ipList/1.html
        http://ip.kxdaili.com/ipList/2.html
        ...
        http://ip.kxdaili.com/ipList/10.html
        '''
        urls = ['http://ip.kxdaili.com/ipList/{}.html'.format(i) for i in range(1,11)]
        for url in urls:
            r = requests.get(url)
            html = HTML(r.text)
            table = html.xpath('//table[@class="ui table segment"]/tbody')[0]
            for tr in table:
                yield tr[0].text + ':' + tr[1].text


    @staticmethod
    def getProxy_seven():
        '''
        中国ip地址
        几乎没有能用的
        https://cn-proxy.com/
        '''
        r = requests.get('https://cn-proxy.com/')
        html = HTML(r.text)
        tables = html.xpath('//table[@class="sortable"]/tbody')
        try:
            table = tables[-1]
            for tr in table:
                yield tr[0].text + ':' + tr[1].text
        except Exception as e:
            print (e)


def test_one_proxy(proxy):
    proxy = {
        'https' : 'https://'+proxy, 
        'http': 'http://'+proxy
    }
    #test_url = 'https://httpbin.org/ip'
    test_url = 'https://passport.weibo.cn/signin/login'
    try:
        r = requests.get(test_url, proxies=proxy, timeout=10)
    except Exception as e:
        print(proxy,"Cannot connect ",e)
        return 
    if r.text.find('密码'):
        #ip = json.loads(r.text).get('origin').split(',')[0]
        #print(r.text)
        return proxy
    else:
        print(p, "status code", r.status_code)
        return None


def testProxyFunction(fun):
    fun_name = getattr(fun, '__name__', "None")
    print('checking function:', fun_name)
    proxies = list(fun())
    for p in proxies:
        res = test_one_proxy(p)
        if res:
            print(p, "  success------->", res)
        else:
            print(p, "  failed")


if __name__ == "__main__":
    #testProxyFunction(GetProxy.getProxy_one)
    #testProxyFunction(GetProxy.getProxy_two)
    testProxyFunction(GetProxy.getProxy_three)
    testProxyFunction(GetProxy.getProxy_four)
    testProxyFunction(GetProxy.getProxy_five)
    testProxyFunction(GetProxy.getProxy_six)
    testProxyFunction(GetProxy.getProxy_seven)
    #print(test_one_proxy,('111.177.185.129' '9999'))
    #ip = input("input ip:").strip()
    #testProxyFunction(GetProxy.getProxy_five)
    #port = input('input prot:').strip()
    #print(test_one_proxy(ip+':'+port))
