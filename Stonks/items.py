# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Ticker(scrapy.Item):
    name = scrapy.Field()
    num_mentions = scrapy.Field()
    pass

class StonksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
