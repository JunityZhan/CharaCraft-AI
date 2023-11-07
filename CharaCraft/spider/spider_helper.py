import os
import re
import sys

from scrapy.crawler import CrawlerProcess
from spider.spiders.wiki_spider import TextSpider


def safe_filename(filename):
    """Return a safe version of the filename by replacing non-alphanumeric characters."""
    disallowed_characters = '<>:"/\\|?*\0'
    return re.sub('[{}]'.format(re.escape(disallowed_characters)), '_', filename)


def main(start_url, max_depth, dynamic):
    output_file_name = safe_filename(os.path.basename(start_url).split('/')[-1]) + '.jsonl'
    output_file = os.path.join('CharaCraft/data', output_file_name)

    settings = {
        'LIMIT_DEPTH': str(max_depth),
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 100,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
        'CONCURRENT_REQUESTS_PER_IP': 100,
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': 0,
        'FEEDS': {
            output_file: {
                'format': 'jsonlines',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 0,
            }
        },
        'ITEM_PIPELINES': {
            'spider.pipelines.GeneralPipeline': 100,
            'spider.pipelines.ConfiguredPipeline': 300,
        },

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # 关闭默认方法
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 1,  # 开启
            'spider.middlewares.RandomHeaderMiddleWare': 545,  # dynamic
        } if dynamic else {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # 关闭默认方法
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 1,  # 开启
        },
    }

    process = CrawlerProcess(settings)
    process.crawl(TextSpider, url=start_url)
    process.start()


if __name__ == '__main__':
    start_url_arg = sys.argv[1]
    max_depth_arg = sys.argv[2]
    dynamic = bool(int(sys.argv[3]))
    main(start_url_arg, max_depth_arg, dynamic)
