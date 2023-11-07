from typing import Optional, Generator, Any, Union, Dict
from urllib.parse import urlparse
import urllib
import scrapy
from scrapy import Spider
from scrapy.http import Response, Request
from scrapy.crawler import Crawler
from ..items import SpiderItem

class TextSpider(Spider):
    name: str = 'text'

    def __init__(self, url: Optional[str] = None, *args: Any, **kwargs: Any) -> None:
        super(TextSpider, self).__init__(*args, **kwargs)
        self.limit_depth = 0
        if url is None:
            raise ValueError('A target URL is required. Use the "url" argument to specify one.')
        self.start_urls = [url]
        self.allowed_domains = [urlparse(url).netloc]

    @classmethod
    def from_crawler(cls, crawler: Crawler, *args: Any, **kwargs: Any) -> Spider:
        spider = super(TextSpider, cls).from_crawler(crawler, *args, **kwargs)
        # Retrieve the depth limit setting
        spider.limit_depth = crawler.settings.getint('LIMIT_DEPTH', default=0)
        return spider

    def parse(self, response: Response) -> Generator[Union[Dict[str, str], Request], None, None]:
        """Extract text from the page and follow links within the allowed domain."""
        # Extract text from the page, excluding content within scripts or hidden elements
        all_text = response.xpath("""
        //body
        //text()[
          not(parent::script) and 
          not(parent::style) and 
          not(parent::link) and 
          not(ancestor::head)
        ]
        """).extract()
        all_text_str = ''.join(all_text).strip()

        # Populate and yield the item
        item = SpiderItem()
        item['url'] = urllib.parse.unquote(response.url)
        item['text'] = all_text_str
        yield item

        # Check the depth of the current page
        current_depth = response.meta.get('depth', 0)
        # Follow links to other pages if the depth is within the limit

        if current_depth < self.limit_depth:
            for href in response.css('a::attr(href)').extract():  # TODO： 允许用户自定义规则
                next_page = urllib.parse.unquote(response.urljoin(href))
                if self.allowed_domains[0] in next_page:
                    yield scrapy.Request(next_page, callback=self.parse)
