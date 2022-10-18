from __future__ import unicode_literals, absolute_import, division, print_function
import re
import retrying
import requests
from fake_useragent import UserAgent
from proxy_scraper.proxy_scraper.Utils import  IPPortPatternGlobal
from utils.logging import get_logger



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
        chars = matchobj.groups()[0].split('+')
        num = ''
        for numOfChars in chars[1:]:
            var1, var2 = numOfChars.strip('()').split('^')
            digit = self.charEqNum[var1] ^ self.charEqNum[var2]
            num += str(digit)
        return num

    @retrying.retry(stop_max_attempt_number=2)
    def extract_pages(self):
        try:
            expSession = r"'([a-z0-9]{32})'"
            url = 'http://spys.one/proxies/'
            rp = requests.get(url, proxies=self.cur_proxy, timeout=10, headers=self.headers)
            page = rp.text

            sessionId = re.findall(expSession, page)[0]
            data = {
                'xf0': sessionId,
                'xpp': 3,
                'xf1': None,
            }
            method = 'POST'
            urls = [
                {'url': url, 'data': {**data, 'xf1': lvl}, 'method': method}
                for lvl in [3, 4]
            ]



        except Exception as e:
            logger.error(f"[-] Request page  error: {e}")
            while self.proxies:
                new_proxy = self.proxies.pop(0)
                self.cur_proxy = {new_proxy['type']: "%s:%s" % (new_proxy['host'], new_proxy['port'])}
                raise e
            else:
                return [], None

        logger.debug(f"[+] Got pages \n {urls}")

        return urls, page

    @retrying.retry(stop_max_attempt_number=3)
    def extract_proxy(self, url):
        try:
            expPortOnJS = r'(?P<js_port_code>(?:\+\([a-z0-9^+]+\))+)'
            expCharNum = r'[>;]{1}(?P<char>[a-z\d]{4,})=(?P<num>[a-z\d\^]+)'
            rp = requests.post(url.get('url'), proxies=self.cur_proxy, timeout=10, headers=self.headers
                               , data=url.get('data'))
            page= rp.text
            res = re.findall(expCharNum, page)
            for char, num in res:
                if '^' in num:
                    digit, tochar = num.split('^')
                    num = int(digit) ^ self.charEqNum[tochar]
                self.charEqNum[char] = int(num)
            page = re.sub(expPortOnJS, self.char_js_port_to_num, page)
            re_ip_result = self.re_ip_port_pattern.findall(page)
            re_ip_result=list(set(re_ip_result))
            if  not len(re_ip_result):
                raise ValueError("empty")
        except Exception as e:
            logger.error("[-] Request page {page} error: {error}")
            while self.proxies:
                new_proxy = self.proxies.pop(0)
                self.cur_proxy = {new_proxy['type']: "%s:%s" % (new_proxy['host'], new_proxy['port'])}
                raise e
            else:
                return []
        re_ip_port_result = []

        for each_result in re_ip_result:
            host, port = each_result
            re_ip_port_result.append({"host": host, "port": int(port), "from": "SpysOne"})

        return re_ip_port_result

    def start(self):
        tuple_unpack= self.extract_pages()
        urls, page= tuple_unpack[0], tuple_unpack[1]

        if urls:
            for url in urls:
                self.result.extend(self.extract_proxy(url))


if __name__ == '__main__':

    p = Proxy()
    p.start()

    for i in p.result:
        print(i)

    print(len(p.result))
