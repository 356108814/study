# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EshipItem(scrapy.Item):
    name = scrapy.Field()
    code = scrapy.Field()
    market = scrapy.Field()
    category = scrapy.Field()
    built_date = scrapy.Field()
    factory = scrapy.Field()
    location = scrapy.Field()
    length = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    load_weight = scrapy.Field()
    level = scrapy.Field()
    zone = scrapy.Field()
    model_type = scrapy.Field()
    price = scrapy.Field()
    seller = scrapy.Field()
    buyer = scrapy.Field()
    trade_desc = scrapy.Field()
    link = scrapy.Field()
