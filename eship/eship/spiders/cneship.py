# encoding: utf-8
"""
船舶成交信息
@author Yuriseus
@create 2016-11-17 15:38
"""
import scrapy
from scrapy_splash import SplashRequest
from eship.items import EshipCJItem


class CneshipSpider(scrapy.Spider):
    name = "cneship"
    allowed_domains = ["cn-eship.com"]

    start_urls = []
    start_id = 25814
    max_id = 30000
    for x in xrange(start_id, max_id, 1):
        url = 'http://www.cn-eship.com/cj/cjinfo.jsp?dbid=%s' % (x + 1)
        start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        print('='*100)
        # print(response.body)
        if response.body.find('信息不存在') != -1:
            return None

        item = EshipCJItem()
        names = item.fields.keys()
        for name in names:
            value = response.xpath("//*[@id='%s']/text()" % name).extract_first()
            if name == 'price':
                value = value.replace(',', '').replace(u'元', '')
            print(name, value)
            item[name] = value

        item['link'] = response.url
        return item

