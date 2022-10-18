# Proxy Scraper 
Proxy Scraper is an open source tool that finds public proxies from multiple sources and asynchronously checks them.

![image](https://github.com/boxxello/Proxy-Scraper-pkg/blob/master/static/demo_gif.gif)

```
pip install -U git+https://github.com/boxxello/Proxy-Scraper-pkg.git
```

Features
--------
-   Support protocols: HTTP(S)
-   Automatically removes duplicate proxies
-   Validates the proxies that are inputted from an input file

Requirements
------------

Python 3.8+
-   [geoip2](https://pypi.org/project/geoip2/)
-   [retrying](https://pypi.org/project/retrying/)
-   [gevent](https://pypi.org/project/gevent/)
-   [fake-useragent](https://pypi.org/project/fake-useragent/)

All the requirements will be installed with the setup.py - or you can manually installed them by running.

```
pip install -r requirements.txt
```

Proxy-Scraper-pkg Hello World
---------

```py
from proxy_scraper.getproxy import GetProxy

proxy_scraper = GetProxy()
proxy_scraper.init()
proxy_scraper.load_input_proxies()
proxy_scraper.validate_input_proxies()
proxy_scraper.load_plugins()
proxy_scraper.grab_web_proxies()
proxy_scraper.validate_web_proxies()
proxy_scraper.save_proxies()
```
either way you can also run it from a console.
<br />
Usage:
```
pyhton -m proxy_scraper [--input name_of_the_file.txt] [--output name_of_the_file2.txt]
                        [--debug]
```

Experiencing issues?
-------------

Make sure that You using latest version!!!
```
pip install -U git+https://github.com/boxxello/Proxy-Scraper-pkg.git
```
TODO
----
-   Save the current ips in a db.
-   Make an API to retrieve the latest scraped ips without having you to run it on your machine.
-   Turn every plugin into an instance of a child which inherits its properties from a father.


Contributing
-------------

-   Fork it: <https://github.com/boxxello/Proxy-Scraper-pkg/fork>
-   Create your feature branch: `git checkout -b MY-NEW-FEATURE`
-   Commit your changes: `git commit -am 'Add some feature'`
-   Push to the branch: `git push origin MY-NEW-FEATURE`
-   Submit a pull request!

License
-------------

Licensed under the Apache License, Version 2.0

-   This product includes GeoLite2 data created by MaxMind, available from* [http://www.maxmind.com](http://www.maxmind.com).
-   This product includes Retrying available from* [Retrying github page](https://github.com/rholder/retrying).
-   This product includes Gevent available from* [Gevent github page](https://github.com/gevent/gevent).
-   This product includes fake-user-agent available from* [fake-user-agent github page](https://github.com/hellysmile/fake-useragent).

Thanks goes to these existing libraries
-------------

-   This product include portions of code from [GetProxy](https://github.com/ywang-wnlo/getproxy).
-   This product include portions of code from [ProxyBroker2](https://github.com/bluet/proxybroker2).


** **_Disclaimer & WARNINGS:_**

1. **Use** this ONLY for **Educational Purposes!** By using this code you agree
   that **I'm not responsible for any kind of trouble** caused by the code. <br>
2. **Make sure web-scraping is legal in your region.**

