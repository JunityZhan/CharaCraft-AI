import os
import re
import sys

from scrapy.crawler import CrawlerProcess
from spider.spiders.wiki_spider import TextSpider


def safe_filename(filename):
    """Return a safe version of the filename by replacing non-alphanumeric characters."""
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', filename)


def main(start_url, max_depth, dynamic):
    output_file_name = safe_filename(os.path.basename(start_url).split('/')[-1]) + '.jsonl'
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    parent_dir = os.path.dirname(parent_dir)
    output_dir = os.path.join(parent_dir, 'data')
    output_file = os.path.join(output_dir, output_file_name)

    settings = {
        'LIMIT_DEPTH': str(max_depth),
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
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/34.0.1847.131 Safari/537.36',

        'DOWNLOADER_MIDDLEWARES': {
            'spider.middlewares.RandomHeaderMiddleWare': 545,
        } if dynamic else {},
    }

    process = CrawlerProcess(settings)
    process.crawl(TextSpider, url=start_url)
    process.start()


if __name__ == '__main__':
    start_url_arg = sys.argv[1]
    max_depth_arg = sys.argv[2]
    dynamic = bool(int(sys.argv[3]))
    main(start_url_arg, max_depth_arg, dynamic)
