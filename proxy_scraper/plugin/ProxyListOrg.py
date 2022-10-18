from __future__ import unicode_literals, absolute_import, division, print_function
import re
from base64 import b64decode
import retrying
import requests
from fake_useragent import UserAgent
from proxy_scraper.proxy_scraper.Utils import IPPortPatternLine
from utils.logging import get_logger

logger = get_logger(__name__)

class Proxy(object):
    def __init__(self):
        self.url = 'http://proxy-list.org/english/index.php?p=1'
        self.re_ip_pattern =  re.compile(r'''Proxy\('([\w=]+)'\)''')
        self.re_ip_port_pattern = IPPortPatternLine
        self.cur_proxy = None
        self.proxies = []
        self.result = []
        self.user_agent= UserAgent()

        self.headers={'User-Agent': self.user_agent.random,
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'accept-encoding': 'gzip, deflate, br',
                       'accept-language': 'en-US,en;q=0.8',
                       "referer": f"https://google.com/"}
    def decode_proxy(self, proxies):
        return [b64decode(hp).decode() for hp in proxies]

    @retrying.retry(stop_max_attempt_number=2)
    def extract_pages(self):
        try:
            exp = r'''href\s*=\s*['"]\./([^'"]?index\.php\?p=\d+[^'"]*)['"]'''

            rp = requests.get(self.url, proxies=self.cur_proxy, timeout=10, headers=self.headers)
            urls = [
                'http://proxy-list.org/english/%s' % path for path in re.findall(exp, rp.text)
            ]
            urls.append(self.url)
            urls = list(set(urls))
        except Exception as e:
            logger.error("[-] Request page {page} error: {error}")
            while self.proxies:
                new_proxy = self.proxies.pop(0)
                self.cur_proxy = {new_proxy['type']: "%s:%s" % (new_proxy['host'], new_proxy['port'])}
                raise e
            else:
                return []
            
        logger.debug(f"[+] Got pages \n {urls}" )
        return urls

    @retrying.retry(stop_max_attempt_number=3)
    def extract_proxy(self, url):
        try:
            rp = requests.get(url, proxies=self.cur_proxy, timeout=10, headers=self.headers)

            re_ip_result = self.re_ip_pattern.findall(rp.text)
            re_port_encode_result=self.decode_proxy(re_ip_result)
            if not len(re_port_encode_result) or not len(re_ip_result):
                raise ValueError("empty")
        except Exception as e:
            logger.error(f"[-] Request page error: {e}")
            while self.proxies:
                new_proxy = self.proxies.pop(0)
                self.cur_proxy = {new_proxy['type']: "%s:%s" % (new_proxy['host'], new_proxy['port'])}
                raise e
            else:
                return []
        re_ip_port_result=[]
        for each_result in re_port_encode_result:

            host, port = each_result.split(':')
            re_ip_port_result.append({"host": host, "port": int(port), "from": "proxylist"})
        return re_ip_port_result

    def start(self):
        urls = self.extract_pages()
        for url in urls:
            self.result.extend(self.extract_proxy(url))



if __name__ == '__main__':

    p = Proxy()
    p.start()

    for i in p.result:
        print(i)

    print(len(p.result))
