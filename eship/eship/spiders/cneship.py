# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class CneshipSpider(scrapy.Spider):
    name = "cneship"
    allowed_domains = ["cn-eship.com"]
    start_urls = (
        'http://www.cn-eship.com/public/PublicInfo.jsp?optid=1490',
    )
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
		print('='*100)
		# print(response.body)
		tables = response.xpath('//table')
		# 编号、市场
		code_t = tables[0]
		code = code_t.xpath('./tbody/tr/td/span/text()').extract_first()
		market = code_t.xpath('./tbody/tr/td[2]/text()').extract_first()

		# 船信息
		ship_t = tables[1]
		name = ship_t.xpath('./tbody/tr[1]/td[1]/text()').extract_first()
		category = ship_t.xpath('./tbody/tr[1]/td[2]/text()').extract_first()
		name = ship_t.xpath('./tbody/tr[1]/td[1]/text()').extract_first()
		category = ship_t.xpath('./tbody/tr[1]/td[2]/text()').extract_first()
		
		built_date = ship_t.xpath('./tbody/tr[2]/td[1]/text()').extract_first()
		factory = ship_t.xpath('./tbody/tr[2]/td[2]/text()').extract_first()

		location = ship_t.xpath('./tbody/tr[3]/td[1]/text()').extract_first()
		length = ship_t.xpath('./tbody/tr[3]/td[2]/text()').extract_first()

		width = ship_t.xpath('./tbody/tr[4]/td[1]/text()').extract_first()
		height = ship_t.xpath('./tbody/tr[4]/td[2]/text()').extract_first()

		weight = ship_t.xpath('./tbody/tr[5]/td[1]/span/text()').extract_first()
		load_weight = ship_t.xpath('./tbody/tr[5]/td[2]/span/text()').extract_first()

		level = ship_t.xpath('./tbody/tr[6]/td[1]/text()').extract_first()
		zone = ship_t.xpath('./tbody/tr[6]/td[2]/text()').extract_first()

		model_type = ship_t.xpath('./tbody/tr[7]/td[1]/text()').extract_first()


		# 价格
		price_t = tables[2]
		price = price_t.xpath('./tbody/tr[2]/td[1]/span/text()').extract_first()


		# 买卖
		trade_t = tables[3]
		seller = trade_t.xpath('./tbody/tr[1]/td[1]/text()').extract_first()
		buyer = trade_t.xpath('./tbody/tr[2]/td[1]/text()').extract_first()
		trade_desc = trade_t.xpath('./tbody/tr[3]/td[1]/text()').extract_first()



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
		print('moel_type:%s' % model_type)
		print('price:%s' % price)
		print('seller:%s' % seller)
		print('buyer:%s' % buyer)
		print('trade_desc:%s' % trade_desc)

		# 船信息
			
		# print(tables)
        #filename = response.url.split("/")[-2] + '.html'
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
