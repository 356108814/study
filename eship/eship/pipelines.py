# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class EshipPipeline(object):
    def __init__(self):
        self.db_path = '/home/dream/github/study/eship/eship.db'
        self.conn = sqlite3.connect(self.db_path)
    
    def open_spider(self, spider):
        if not path.exists(self.db_path):
            self.conn.execute("""create table ship(id integer primary key autoincrement, name text, code text, market text)""")
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.conn.execute('insert into ship values(?,?,?,?)',(None, item['name'], item['code'], item['market'])
        return item
