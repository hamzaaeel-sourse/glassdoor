# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class GlassdoorPipeline:
    def process_item(self, item, spider):
        return item


class ExcelPipeline:
    def open_spider(self, spider):
        self.jobs = []

    def close_spider(self, spider):
        df = pd.DataFrame(self.jobs)
        df.to_excel('jobs.xlsx', index=False)

    def process_item(self, item, spider):
        self.jobs.append(item)
        return item
