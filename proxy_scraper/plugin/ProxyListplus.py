from __future__ import unicode_literals, absolute_import, division, print_function
from itertools import chain
import retrying
import requests
from fake_useragent import UserAgent
from proxy_scraper.proxy_scraper.Utils import IPPortPatternGlobal
from utils.logging import get_logger


logger = get_logger(__name__)


class Proxy(object):
    def __init__(self):
        self.url='http://list.proxylistplus.com/%s-List-%d'
        self.re_ip_port_pattern = IPPortPatternGlobal
        self.cur_proxy = None
        self.proxies = []
        self.result = []
        self.user_agent = UserAgent()

        self.headers = {'User-Agent': self.user_agent.random,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'accept-encoding': 'gzip, deflate',
                        'accept-language': 'en-US,en;q=0.8',
                        "referer": f"https://google.com/"}
    def extract_pages(self):
        names = ['Fresh-HTTP-Proxy']
        #you can also extract ssl/socks5 proxy
        urls = [
            'http://list.proxylistplus.com/%s-List-%d' % (i, n)
            for i in names
            for n in range(1, 7)
        ]
        return urls

    @retrying.retry(stop_max_attempt_number=3)
    def extract_proxy(self, url):
        try:
            rp = requests.get(url, proxies=self.cur_proxy, timeout=10, headers=self.headers)
            page = rp.text
            re_ip_result = self.re_ip_port_pattern.findall(page)
            re_ip_result=list(set(pair for pair in re_ip_result if pair[1] != ''))
            logger.info(f"[+] Got {len(re_ip_result)} proxies from {url}")

            if  not len(re_ip_result):
                raise ValueError("empty")
        except Exception as e:
            logger.error(f"[-] Request page : {e}")
            while self.proxies:
                new_proxy = self.proxies.pop(0)
                self.cur_proxy = {new_proxy['type']: "%s:%s" % (new_proxy['host'], new_proxy['port'])}
                raise e
            else:
                return []
        re_ip_port_result = []

        for each_result in re_ip_result:
            host, port = each_result
            re_ip_port_result.append({"host": host, "port": int(port), "from": "ProxyListPlus"})
        return re_ip_port_result

    def start(self):

        self.result.extend(chain.from_iterable([self.extract_proxy(url) for url in self.extract_pages()]))





if __name__ == '__main__':

    p = Proxy()
    p.start()

    for i in p.result:
        print(i)


    print(len(p.result))
