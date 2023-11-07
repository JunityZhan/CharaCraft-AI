import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    text = scrapy.Field()
    url = scrapy.Field()
