from __future__ import unicode_literals, absolute_import, division, print_function
import logging
import retrying
import requests
from fake_useragent import UserAgent

from proxy_scraper.proxy_scraper.Utils import  IPPortPatternLine

logger = logging.getLogger(__name__)


class Proxy(object):
    def __init__(self):
        self.re_ip_port_pattern=IPPortPatternLine
        self.cur_proxy = None
        self.proxies = []
        self.result = []


        self.txt_list=[
            'http://static.fatezero.org/tmp/proxy.txt',
            'http://pubproxy.com/api/proxy?limit=20&format=txt&type=http',

            'http://www.proxylists.net/http_highanon.txt',
            'http://www.proxylists.net/http.txt',
            'http://ab57.ru/downloads/proxylist.txt',

            'https://api.proxyscrape.com/?request=getproxies&proxytype=http',
            'http://ipaddress.com/proxy-list/',
            'https://www.sslproxies.org/',
            'https://free-proxy-list.net/',
            'https://us-proxy.org/',
            'http://www.httptunnel.ge/ProxyListForFree.aspx',
        ]

    @retrying.retry(stop_max_attempt_number=3)
    def extract_proxy(self, url, user_agent):
        try:
            # we don't need br as accept-encoding. it will cause error when downloading file and decoding it.
            headers = {'User-Agent': user_agent,
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'accept-encoding': 'gzip, deflate',

                       'accept-language': 'en-US,en;q=0.8',
                       "referer": f"https://google.com/"}
            rp = requests.get(url, proxies=self.cur_proxy, headers=headers, timeout=10)
            if rp.status_code == 200:
                re_ip_port_result = self.re_ip_port_pattern.findall(rp.text)
                if not re_ip_port_result:
                    raise Exception("empty")

        except Exception as e:
            logger.error("[-] Request url {url} error: {error}".format(url=url, error=str(e)))
            while self.proxies:
                new_proxy = self.proxies.pop(0)
                self.cur_proxy = {new_proxy['type']: "%s:%s" % (new_proxy['host'], new_proxy['port'])}
                raise e
            else:
                return []

        return [{'host': host, 'port': int(port), 'from': 'txt'} for host, port in re_ip_port_result]

    def start(self):
        ua = UserAgent()

        for url in self.txt_list:
            try:
                page_result = self.extract_proxy(url, ua.random)
            except:
                continue

            if not page_result:
                continue

            self.result.extend(page_result)


if __name__ == '__main__':
    p = Proxy()
    p.start()

    for i in p.result:
        print(i)

    print(len(p.result))
