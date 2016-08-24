# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .db.db_mongo import DBMongo


class JobPipeline(object):
    def __init__(self):
        self.db_mongo = DBMongo('172.16.1.206', 27017, 'lagou')

    def process_item(self, item, spider):
        collection_name = 'job'
        self.db_mongo.insert(collection_name, dict(item))
        return item
