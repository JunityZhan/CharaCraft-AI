BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

ROBOTSTXT_OBEY = False
HTTPERROR_ALLOWED_CODES  =[404]
CONCURRENT_REQUESTS = 100
REACTOR_THREADPOOL_MAXSIZE = 20
ITEM_PIPELINES = {
    'spider.pipelines.GeneralPipeline': 100,
    'spider.pipelines.ConfiguredPipeline': 300,
}
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
# Set settings whose default value is deprecated to a future-proof value
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