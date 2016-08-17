# coding:utf-8
from .util import ParserUtil


class Parser(object):
    """
    日志解析器基类
    """
    def __init__(self):
        self.raw_data = None
        self._util = ParserUtil
        self.init()

    def init(self):
        pass

    def process(self, data):
        """
        开始处理
        :param data:
        :return: 解析结果
        """
        self.raw_data = data
        return self.raw_data


