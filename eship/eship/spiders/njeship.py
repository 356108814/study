# encoding: utf-8
"""
南京船舶交易市场成交信息
@author Yuriseus
@create 2020-03-13 21:38
"""
import scrapy
from scrapy_splash import SplashRequest

from eship.adpater import Adapter


class CneshipSpider(scrapy.Spider):
    name = "njeship"
    allowed_domains = ["njcbjysc.com"]

    start_urls = []
    start_id = 1190
    max_id = 10000
    for x in range(start_id, max_id, 1):
        url = 'http://www.njcbjysc.com/cjxx/%s.jhtml' % (x + 1)
        start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        print('=' * 100)
        if response.body.find('信息不存在') != -1:  # TODO 判断信息不存在
            return None
        selectors = response.xpath('//tr/td/text()')
        data = []
        for i, s in enumerate(selectors):
            text = s.get().replace('\xa0', '').replace('\n', '').replace(' ', '')  # 替换&nbsp;
            data.append(text)
        if len(data) != 33:
            return None
        item = Adapter.nj_to_EshipCJItem(data)
        item['link'] = response.url
        return item
