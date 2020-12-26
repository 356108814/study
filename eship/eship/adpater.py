# coding: utf-8
from eship.items import EshipCJItem


class Adapter(object):
    """适配器，不同平台的数据格式转换为数据库表中的格式"""

    @staticmethod
    def nj_to_EshipCJItem(data):
        """
        南京数据转换为存储的
        ：param data 数组，长度32，内容见 nj/data文件
        """
        key_dict = {
            'dbid': 1,  # 编号
            'price': 3,  # 成交价格
            'shiptype': 5,  # 船舶类型
            'cdate': 7,  # 成交日期
            'dwt': 9,  # 载重吨
            'sr': 11,  # 航区
            'scp': 13,  # 建造地点
            'sregp': 15,  # 船籍港
            'sclass': 17,  # 船级
            'gt': 19,  # 总吨
            'scd': 21,  # 建造日期
            'loa': 23,  # 总长
            'bm': 25,  # 型宽
            'dm': 27,  # 型深
            'mt': 29,  # 主机型号
            'remark': 31,  # 备注
        }
        item = EshipCJItem()
        for name in key_dict:
            item[name] = data[key_dict[name]]
        return item
