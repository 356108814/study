# coding: utf-8


from scrapy import Selector
from eship.adpater import Adapter


if __name__ == '__main__':
    body = open('ship_nj.html', encoding='utf-8').read()
    selector = Selector(text=body)
    selectors = selector.xpath('//tr/td/text()')
    print(len(selectors))
    data = []
    for i, s in enumerate(selectors):
        text = s.get().replace('\xa0', '').replace('\n', '').replace(' ', '')    # 替换&nbsp;
        print(str(i) + ':' + text)
        data.append(text)

    print(Adapter.nj_to_EshipCJItem(data))


