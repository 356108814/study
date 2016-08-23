# encoding: utf-8
"""
服务信息
@author Yuriseus
@create 2016-8-18 10:15
"""


class Service(object):
    def __init__(self):
        self.name = ''
        self.path = ''
        self.version = 1
        self.is_start = 0
        self.is_from_dir = 1    # 数据来源是否为文件夹
        self.dir_path = ''      # 数据来源文件夹路径
        self.instance = None    # 服务实例

    def __eq__(self, obj):
        return str(self) == str(obj)

    def __str__(self):
        return '%s_%s_%s' % (self.path, self.version, self.is_start)
