BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

ROBOTSTXT_OBEY = False
HTTPERROR_ALLOWED_CODES = [404]
CONCURRENT_REQUESTS = 100
DOWNLOAD_DELAY = 0
REACTOR_THREADPOOL_MAXSIZE = 20
ITEM_PIPELINES = {
    'spider.pipelines.GeneralPipeline': 100,
    'spider.pipelines.ConfiguredPipeline': 300,
}
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # 关闭默认方法
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 1,  # 开启
}
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEEDS = {
    'output.jsonl': {
        'format': 'jsonlines',  # Using JSON Lines format for simplicity
        'encoding': 'utf8',
        'store_empty': False,
        'fields': None,
        'indent': 0,
    },
}
