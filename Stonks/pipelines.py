# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy import exceptions
#import itertools
from pydispatch import dispatcher
class TickerPipeline:

    def __init__(self):
        self.tickers_seen = set()
        self.ticker_export = {} #dictionary of ticker items
        self.ticker_ignore = ['YOLO', 'DD', 'WSB', 'HODL', 'MOON',
        'FUCK', 'SHIT', 'IED', 'CEO', 'PTSD', 'AF', 'US', 'TV', 'USD', 'YOU',
        'ALL', 'WITH', 'APES', 'ON', 'ONE', 'WHAT', 'AN', 'EXIT', 'DFV', 'EDIT',
        'THEY', 'HIM', 'HE', 'WE', 'HOLD', 'DID', 'TO', 'THE', 'BOYS', 'IN',
        'RIDE', 'FCKT', 'LMAO', 'LOL', 'THAT', 'RIP']

    def open_spider(self, spider):
        f = open("results.csv", "ab+")
        self.ticker_exporter = scrapy.exporters.CsvItemExporter(f)
        self.ticker_exporter.start_exporting()
        dispatcher.connect(self.export_items, scrapy.signals.engine_stopped)

    def close_spider(self, spider):
        self.ticker_exporter.finish_exporting()
        pass

    def process_item(self, item, spider):
        #adapter = ItemAdapter(item)
        if item['name'][0] not in self.ticker_ignore:
            if item['name'][0] in self.tickers_seen:
                item['num_mentions'][0] += 1 #increment num_mentions if already seen
                self.ticker_export[item['name'][0]] = item #dictionary updated with new value
                raise exceptions.DropItem()
                pass
            else:
                self.tickers_seen.add(item['name'][0]) #if not seen, add to set
                self.ticker_export[item['name'][0]] = item #add to dictionary
                return item
            pass

        raise exceptions.DropItem() #drop item if in ignore list
        pass

    def export_items(self):
        for ticker in self.ticker_export.values():
            ticker['name'] = ticker['name'][0]
            ticker['num_mentions'] = ticker['num_mentions'][0]
            self.ticker_exporter.export_item(ticker)
            pass
        pass

    pass

class StonksPipeline:
    def process_item(self, item, spider):
        return item
