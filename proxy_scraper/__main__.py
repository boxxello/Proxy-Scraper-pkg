import argparse
import logging

from proxy_scraper.getproxy import GetProxy
from argparse import Namespace

from proxy_scraper.loggers import get_logger

logger=get_logger(__name__)
def enable_debug_logging() -> None:
    """
    Enable debug logging for the scripts

    :return: None
    """
    logger.setLevel(logging.DEBUG)
    for handler in logger.handlers:
        handler.setLevel(logging.DEBUG)
    logger.info(f"Enabled debug logging")
def parse_args()->Namespace:
    parser = argparse.ArgumentParser(description='Proxy Scraper')
    parser.add_argument(
        "--input",
        required=False,
        type=str,
        help="Input file",
    )
    parser.add_argument(
        "--output",
        required=False,
        type=str,
        help="Output file",
    )
    parser.add_argument(
        "--debug",
        type=bool,
        default=True,
        help="Enable debug logging",
    )

    args = parser.parse_args()
    logger.info(args)

    return args

if __name__ == '__main__':
    args = parse_args()
    if args.debug:
        enable_debug_logging()
    proxy_scraper = GetProxy(
        input_proxies_file=args.input,
        output_proxies_file=args.output,
    )
    proxy_scraper.init()
    proxy_scraper.load_input_proxies()
    proxy_scraper.validate_input_proxies()
    proxy_scraper.load_plugins()
    proxy_scraper.grab_web_proxies()
    proxy_scraper.validate_web_proxies()
    proxy_scraper.save_proxies()
