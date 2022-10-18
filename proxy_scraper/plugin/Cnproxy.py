from __future__ import unicode_literals, absolute_import, division, print_function
import re
import time
import retrying
import requests
from fake_useragent import UserAgent
from utils.logging import get_logger


logger = get_logger(__name__)


class Proxy(object):
    def __init__(self):
        self.url = 'http://www.cnproxy.com/proxy{page}.html'
        self.re_ip_pattern = re.compile(r'<tr><td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})<SCRIPT', re.I)
        self.re_port_encode_pattern = re.compile(r'javascript>document.write\(":"([+\w]{2,10})\)</SCRIPT>', re.I)

        self.port_dict = {
            'v': '3',
            'm': '4',
            'a': '2',
            'l': '9',
            'q': '0',
            'b': '5',
            'i': '7',
            'w': '6',
            'r': '8',
            'c': '1',
            '+': ''
        }

        self.cur_proxy = None
        self.proxies = []
        self.result = []


    @retrying.retry(stop_max_attempt_number=3)
    def extract_proxy(self, page_num, user_agent):


        try:

            headers={'User-Agent': user_agent,
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'en-US,en;q=0.8',
                        "referer": f"https://google.com/"}

            rp=requests.get(self.url.format(page=page_num), proxies=self.cur_proxy, timeout=10, headers=headers)

            re_ip_result = self.re_ip_pattern.findall(rp.text)
            re_port_encode_result = self.re_port_encode_pattern.findall(rp.text)

            if not len(re_ip_result) or not len(re_port_encode_result):
                raise Exception("empty")

            if len(re_ip_result) != len(re_port_encode_result):
                raise Exception("len(host) != len(port)")

        except Exception as e:
            logger.error(f"[-] Request page {page_num} error: {e}")
            while self.proxies:
                new_proxy = self.proxies.pop(0)
                self.cur_proxy = {new_proxy['type']: "%s:%s" % (new_proxy['host'], new_proxy['port'])}
                raise e
            else:
                return []

        re_port_result = []

        for each_result in re_port_encode_result:
            each_result = each_result.strip()
            re_port_result.append(int(''.join(list(map(lambda x: self.port_dict.get(x, ''), each_result)))))
            # logger.debug(f"Printing each result {each_result}")
            # logger.debug(f"printing re_port_result {int(''.join(list(map(lambda x: self.port_dict.get(x, ''), each_result))))}")

        result_dict = dict(zip(re_ip_result, re_port_result))
        return [{"host": host, "port": int(port), "from": "cnproxy"} for host, port in result_dict.items()]

    def start(self):
        ua = UserAgent()
        for page in range(1, 10):
            logger.info(f"[+] Start to extract proxy from cnproxy, page: {page}")
            page_result = self.extract_proxy(page, ua.random)
            time.sleep(3)

            if not page_result:
                return

            self.result.extend(page_result)


if __name__ == '__main__':

    p = Proxy()
    p.start()

    for i in p.result:
        print(i)

    print(len(p.result))
