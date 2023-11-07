from typing import Any, Optional
from random import random
from scrapy import signals
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse, Request, Response
from selenium import webdriver
from scrapy.spiders import Spider
from scrapy.crawler import Crawler


def process_exception(request: Request, exception: Exception, spider: Spider) -> Optional[Response]:
    return None


def process_response(request: Request, response: Response, spider: Spider) -> Response:
    return response


class RandomHeaderMiddleWare:
    def __init__(self) -> None:
        self.user_agents = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/118.0.0.0 Safari/537.36')

    def process_request(self, request: Request, spider: Spider) -> HtmlResponse:
        request.headers['User-Agent'] = self.user_agents
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        option.add_argument('no-sandbox')
        option.add_argument('disable-blink-features=AutomationControlled')
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(options=option)

        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
              '''
        })
        driver.get(request.url)
        driver.implicitly_wait(5)
        content = driver.page_source
        driver.quit()
        return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
