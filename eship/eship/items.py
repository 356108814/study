# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EshipPublicItem(scrapy.Item):
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


class EshipCJItem(scrapy.Item):
    """
    成交信息，字段与网页对应id一致
    """
    dbid = scrapy.Field()    # 编号
    pid = scrapy.Field()     # 鉴定机构
    shipname = scrapy.Field()    # 名称
    shiptype = scrapy.Field()    # 类型
    scd = scrapy.Field()    # 建造日期
    scp = scrapy.Field()    # 造船厂
    sregp = scrapy.Field()  # 地区
    loa = scrapy.Field()    # 载重
    bm = scrapy.Field()
    dm = scrapy.Field()
    gt = scrapy.Field()
    dwt = scrapy.Field()    # 吨位
    sclass = scrapy.Field()
    sr = scrapy.Field()
    mt = scrapy.Field()
    cdate = scrapy.Field()
    adate = scrapy.Field()
    price = scrapy.Field()
    seller = scrapy.Field()
    remark = scrapy.Field()
    link = scrapy.Field()
