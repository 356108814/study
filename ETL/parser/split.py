# encoding: utf-8

from base import Parser


class SplitParser(Parser):
    """
    分割解析器
    """
    def __init__(self):
        super(SplitParser, self).__init__()

    def split(self, data, sep='|'):
        """
        分割
        :param data:
        :param sep:
        :return: list
        """
        if data is not None and data != '':
            return data.split(sep)
        return []

    def split_k_v(self, data, sep='&', kv_sep='='):
        """
        分割键值对
        :param data:
        :param sep: 分隔符
        :param kv_sep: 键值分割符
        :return: dict
        """
        result_dict = {}
        if data is not None and data != '':
            array = data.split(sep)
            for _, kv in enumerate(array):
                if kv != '':
                    kv_array = kv.split(kv_sep)
                    k = kv_array[0]
                    if len(kv_array) == 2:
                        v = kv_array[1]
                    else:
                        v = ''
                    result_dict[k] = v
        return result_dict


if __name__ == '__main__':
    s = 'aimei_rsp_time=&a=1'
    parser = SplitParser()
    # print parser.split_k_v(s)
    a,b,c = ['a', 'b', 'c']
    print b