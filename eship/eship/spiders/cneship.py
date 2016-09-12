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
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
