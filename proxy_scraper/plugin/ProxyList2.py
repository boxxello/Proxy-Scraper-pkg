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
        self.url='https://webanetlabs.net/publ/24'
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
        urls = [
            'https://www.proxy-list.download/api/v1/get?type=http',
            'https://www.proxy-list.download/api/v1/get?type=https',
            'https://www.proxy-list.download/api/v1/get?type=socks4',
            'https://www.proxy-list.download/api/v1/get?type=socks5',
        ]
        print(urls)

        return urls

    @retrying.retry(stop_max_attempt_number=3)
    def extract_proxy(self, url):
        try:
            rp = requests.get(url, proxies=self.cur_proxy, timeout=10, headers=self.headers)
            page = rp.text
            re_ip_result = self.re_ip_port_pattern.findall(page)

            logger.info(f"[+] Got {len(re_ip_result)} proxies from {url}")
            re_ip_result=list(set(re_ip_result))
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
            re_ip_port_result.append({"host": host, "port": int(port), "from": "Proxy-listDownload"})
        return re_ip_port_result

    def start(self):

        self.result.extend(chain.from_iterable([self.extract_proxy(url) for url in self.extract_pages()]))





if __name__ == '__main__':

    p = Proxy()
    p.start()

    for i in p.result:
        print(i)


    print(len(p.result))
