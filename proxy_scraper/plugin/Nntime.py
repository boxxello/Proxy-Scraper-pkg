from __future__ import unicode_literals, absolute_import, division, print_function
import re
from itertools import chain
import retrying
import requests
from fake_useragent import UserAgent
from proxy_scraper.Utils import  IPPortPatternGlobal

from proxy_scraper.loggers import get_logger

logger = get_logger(__name__)


class Proxy(object):
    charEqNum = {}
    def __init__(self):

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

    def char_js_port_to_num(self, matchobj):
        chars = matchobj.groups()[0]
        num = ''.join([self.charEqNum[ch] for ch in chars if ch != '+'])
        return num
    def extract_pages(self):
        tpl = 'http://www.nntime.com/proxy-updated-{:02}.htm'
        urls = [tpl.format(n) for n in range(1, 31)]
        return urls

    @retrying.retry(stop_max_attempt_number=3)
    def extract_proxy(self, url):
        try:
            rp = requests.get(url, proxies=self.cur_proxy, timeout=10, headers=self.headers)
            page = rp.text
            expPortOnJS = r'\(":"\+(?P<chars>[a-z+]+)\)'
            expCharNum = r'\b(?P<char>[a-z])=(?P<num>\d);'
            self.charEqNum = {char: i for char, i in re.findall(expCharNum, page)}
            page = re.sub(expPortOnJS, self.char_js_port_to_num, page)
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
            re_ip_port_result.append({"host": host, "port": int(port), "from": "Nntime"})
        return re_ip_port_result

    def start(self):

        self.result.extend(chain.from_iterable([self.extract_proxy(url) for url in self.extract_pages()]))





if __name__ == '__main__':

    p = Proxy()
    p.start()

    for i in p.result:
        logger.debug(i)


    logger.debug(len(p.result))
