import scrapy
import re
import itertools
import sys
from ..items import Ticker
from ..pipelines import TickerPipeline
from scrapy.loader import ItemLoader
from scrapy.shell import inspect_response

class StonksSpider(scrapy.Spider):
    name = "Stonks"
    start_urls = ["https://www.reddit.com/r/wallstreetbets/"]
    allowed_domains = ['reddit.com']
    #Stonks = dict()

    #def from_crawler(self, *args, **kwargs):
        #spider = super(scrapy.Spider).from_crawler(cls, crawler, *args, **kwargs)

        #return spider
        #pass

    #def parse_ticker(self, response):

        #pass

    def parse(self, response):
        titles = response.xpath("//h3/text()").re(r"\b\$?[A-Z]{2,4}\b")
        paragraphs = response.xpath("//p/text()").re(r"\b\$?[A-Z]{2,4}\b")
        tickersList = titles + paragraphs

        '''drop $ so strings are purely alphabetical'''
        for ticker in tickersList:
            loader = ItemLoader(item=Ticker(), response=response)
            ticker = ticker.strip()
            if ticker[0] == "$":
                ticker = ticker[1:]
            loader.add_value('name', ticker)
            loader.add_value('num_mentions', 1)
            yield loader.load_item()
            pass

        anchors = response.xpath(".//a[contains(@data-click-id, 'body')]")
        if anchors != None:
            anchors.getall()
            for anchor in anchors:
                new_page = "https://www.reddit.com" + anchor.xpath('@href').get()
                yield scrapy.Request(new_page, callback=self.parse)
                pass
            pass
        pass

    pass



'''NOTES BELOW  vvv'''
'''from itemadapter import ItemAdapter
from scrapy.exporters import XmlItemExporter

class PerYearXmlExportPipeline:
    """Distribute items across multiple XML files according to their 'year' field"""

    def open_spider(self, spider):
        self.year_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.year_to_exporter.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item):
        adapter = ItemAdapter(item)
        year = adapter['year']
        if year not in self.year_to_exporter:
            f = open(f'{year}.xml', 'wb')
            exporter = XmlItemExporter(f)
            exporter.start_exporting()
            self.year_to_exporter[year] = exporter
        return self.year_to_exporter[year]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
'''
