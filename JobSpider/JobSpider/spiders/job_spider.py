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
        job_detail = response.xpath('//dl[@class="job_detail"]')[0]
        print('='*100)
        title = job_detail.xpath('./dt/h1')[0].xpath('@title').extract_first()   # get获取属性
        print('title:%s' % title)
        job_request = response.xpath('//dd[@class="job_request"]')[0]
        spans = job_request.xpath('./p')[0].xpath('./span')    # ./表示从当前节点开始查找
        salary = spans[0].xpath('./text()').extract_first()
        location = spans[1].xpath('./text()').extract_first()

        job_bt = response.xpath('//dd[@class="job_bt"]')[0]
        descs = []
        description = job_bt.xpath('./p')
        # 岗位描述和要求以<p><br></p>隔开，text为None
        is_desc = True
        requirements = []
        for d in description:
            text = d.xpath('./text()').extract_first()
            if text:
                if is_desc:
                    descs.append(text)
                else:
                    if text != u'岗位要求：':
                        requirements.append(text)
            else:
                is_desc = False
        print title
        print salary
        print location
        print descs
        print requirements
        return item
