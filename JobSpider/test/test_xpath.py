# encoding: utf-8
"""
xpath
@author Yuriseus
@create 2016-8-22 17:39
"""
from lxml import etree


def main():
    with open('job.html', 'r') as f:
        content = f.read()
        root = etree.HTML(content)
        job_detail = root.xpath('//dl[@class="job_detail"]')[0]
        title = job_detail.xpath('./dt/h1')[0].get('title', '')    # get获取属性
        job_request = root.xpath('//dd[@class="job_request"]')[0]
        spans = job_request.xpath('./p')[0].xpath('./span')    # ./表示从当前节点开始查找
        salary = spans[0].text
        location = spans[1].text

        job_bt = root.xpath('//dd[@class="job_bt"]')[0]
        descs = []
        description = job_bt.xpath('./p')
        # 岗位描述和要求以<p><br></p>隔开，text为None
        is_desc = True
        requirements = []
        for d in description:
            text = d.text
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


if __name__ == '__main__':
    main()
