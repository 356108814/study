# encoding: utf-8
"""
职位
@author Yuriseus
@create 2016-8-22 17:21
"""

import scrapy
from ..items import JobspiderItem


class LagouJobSpider(scrapy.Spider):
    name = "lagou"
    allowed_domains = ["lagou.com"]
    start_urls = [
        "http://www.lagou.com/jobs/2257216.html",
        # "http://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        item = JobspiderItem()
        item.name = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item.salary = response.xpath('//td[@id="item_name"]/text()').extract()
        # item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item
