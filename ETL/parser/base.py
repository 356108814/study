# coding:utf-8


class Parser(object):
    """
    日志解析器基类
    """
    def __init__(self):  
        """
        初始化
        """
        self.reset()
   
    def reset(self):  
        """
        重置
        """  
        self.rawdata = ''
   
    def feed(self, data):
        """
        提供数据
        :param data: 原始数据
        """
        self.rawdata = self.rawdata + data
        self.handle(self.rawdata)

    def handle(self, data):
        """
        开始处理
        :param data:
        :return: 解析结果
        """
        return ''
   
    def close(self):  
        """
        关闭，停止解析
        """  
        pass 
   
    def getpos(self):
        """
        获取错误发生位置
        """
        return 0, 0

    def error(self, message):  
        raise ParseError(message, self.getpos()) 


class ParseError(Exception):  
    """
    解析错误基类
    """  
   
    def __init__(self, msg, position=(None, None)):  
        assert msg  
        self.msg = msg  
        self.lineno = position[0]  
        self.offset = position[1]  
   
    def __str__(self):  
        result = self.msg  
        if self.lineno is not None:
            result += ", at line %d" % self.lineno
        if self.offset is not None:
            result += ", column %d" % (self.offset + 1)
        return result  
