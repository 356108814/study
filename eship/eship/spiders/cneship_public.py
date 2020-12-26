# encoding: utf-8
"""
船舶公开信息
@author Yuriseus
@create 2016-11-17 15:38
"""

import scrapy
from scrapy_splash import SplashRequest
from eship.items import EshipPublicItem


class CneshipPublicSpider(scrapy.Spider):
    name = "cneship_public"
    allowed_domains = ["cn-eship.com"]

    start_urls = []
    max_id = 30000
    for x in range(max_id):
        url = 'http://www.cn-eship.com/public/PublicInfo.jsp?optid=%s' % (x + 1)
        start_urls.append(url)
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        print('='*100)
        # print(response.body)
        if response.body.find('信息不存在') != -1:
            return
        
        tables = response.xpath('//table')
        # 编号、市场
        code_t = tables[0]
        code = code_t.xpath('./tbody/tr/td/span/text()').extract_first()
        market = code_t.xpath('./tbody/tr/td[2]/text()').extract_first()
        market = market.replace(u'市场：', '')

        # 船信息
        ship_t = tables[1]
        name = ship_t.xpath('./tbody/tr[1]/td[1]/text()').extract_first()
        name = name.replace(u'船名：', '')
        category = ship_t.xpath('./tbody/tr[1]/td[2]/text()').extract_first()
        category = category.replace(u'船型：', '')

        built_date = ship_t.xpath('./tbody/tr[2]/td[1]/span/text()').extract_first()
        factory = ship_t.xpath('./tbody/tr[2]/td[2]/text()').extract_first()
        factory = factory.replace(u'建造船厂：', '')

        location = ship_t.xpath('./tbody/tr[3]/td[1]/text()').extract_first()
        location = location.replace(u'船籍港：', '')

        length = ship_t.xpath('./tbody/tr[3]/td[2]/text()').extract_first()

        width = ship_t.xpath('./tbody/tr[4]/td[1]/text()').extract_first()
        height = ship_t.xpath('./tbody/tr[4]/td[2]/text()').extract_first()
        length = length.replace(u'型长(米)：', '')
        width = width.replace(u'型宽(米)：', '')
        height = height.replace(u'型深(米)：', '')

        weight = ship_t.xpath('./tbody/tr[5]/td[1]/span/text()').extract_first()
        load_weight = ship_t.xpath('./tbody/tr[5]/td[2]/span/text()').extract_first()

        level = ship_t.xpath('./tbody/tr[6]/td[1]/text()').extract_first()
        zone = ship_t.xpath('./tbody/tr[6]/td[2]/text()').extract_first()

        model_type = ship_t.xpath('./tbody/tr[7]/td[1]/text()').extract_first()

        level = level.replace(u'船级：', '')
        zone = zone.replace(u'航区：', '')
        model_type = model_type.replace(u'主机型号：', '')

        # 价格
        price_t = tables[2]
        price = price_t.xpath('./tbody/tr[2]/td[1]/span/text()').extract_first()
        price = price.replace(u',', '').replace(u'元', '')

        # 买卖
        trade_t = tables[3]
        seller = trade_t.xpath('./tbody/tr[1]/td[1]/text()').extract_first()
        buyer = trade_t.xpath('./tbody/tr[2]/td[1]/text()').extract_first()
        trade_desc = trade_t.xpath('./tbody/tr[3]/td[1]/text()').extract_first()
        url = response.url

        print('name:%s' % name)
        print('code:%s' % code)
        print('market:%s' % market)
        print('category:%s' % category)
        print('built_date:%s' % built_date)
        print('factory:%s' % factory)
        print('location:%s' % location)
        print('length:%s' % length)
        print('width:%s' % width)
        print('height:%s' % height)
        print('weight:%s' % weight)
        print('load_weight:%s' % load_weight)
        print('level:%s' % level)
        print('zone:%s' % zone)
        print('model_type:%s' % model_type)
        print('price:%s' % price)
        print('seller:%s' % seller)
        print('buyer:%s' % buyer)
        print('trade_desc:%s' % trade_desc)
        item = EshipPublicItem()
        item['name'] = name
        item['code'] = code
        item['market'] = market
        item['category'] = category
        item['built_date'] = built_date
        item['factory'] = factory
        item['location'] = location
        item['length'] = length
        item['width'] = width
        item['height'] = height
        item['weight'] = weight
        item['load_weight'] = load_weight
        item['level'] = level
        item['zone'] = zone
        item['model_type'] = model_type
        item['price'] = price
        item['seller'] = seller
        item['buyer'] = buyer
        item['trade_desc'] = trade_desc
        item['link'] = url
        return item

