# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

from os import path
from db import DBSqlite


class EshipPipeline(object):
    def __init__(self):
        self.db_path = '/home/dream/github/study/eship/eship.db'
        self.db = DBSqlite(self.db_path)
    
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        columns = ', '.join(item.keys())
        value_list = []
        for column in columns:
            value = item[column]
            if column in ['length', 'width', 'height', 'weight', 'load_weight', 'price']:
                value = value
            else:
                value = "'%s'" % value
        values = ', '.join(value_list)
        sql = 'insert into ship (%s) values(%s)' % (columns, values)
        self.db.save(sql)
        return item
