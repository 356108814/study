# encoding: utf-8
"""
用户行为
@author Yuriseus
@create 2016-8-17 15:14
"""
import time

import settings
from util.date import DateUtil
from util.socket import SocketUtil
from ..base_file import BaseFileService
from ..enums import Product
from ..enums import Terminal


class UserActionService(BaseFileService):

    def __init__(self, dir_path):
        # if not dir_path:
        #     class_path = __name__ + '.' + self.__class__.__name__
        super().__init__(dir_path)
        self.batch_lines_count = 10000
        self._t1 = 0
        self._t_index = 0

    def is_need_drop(self, line_data):
        if line_data.find('uid') == -1:
            return True
        return False

    def get_clean_data(self, line_data):
        # 去除日志前缀
        index = line_data.find(']')
        line_data = (line_data[index+1:]).strip()
        return line_data

    def process(self, lines):
        # 格式：[I 160824 08:15:27 album_handler:99] {"action_time": 1471997727, "songid": 5485700, "uid": 1364881, "ip": "172.16.30.3", "action": 0, "aimei_object": "album", "source": "album_out", "albumid": 598008, "puid": 0}
        if self._t_index == 0:
            self._t1 = time.time()
        column_values = []
        for line in lines:
            column_value = self.get_column_value(line)
            column_values.append(column_value)

        self.insert_many(column_values)
        self.insert_total_many(column_values)

        if settings.DEBUG:
            self._t_index += self.batch_lines_count
            if self._t_index == 280000:
                print('total time: %s' % (time.time() - self._t1))

    def get_column_value(self, line):
        """
        根据行数据获取需要插入到数据库的字典
        :param line:
        :return:
        """
        data = self.parser.get_dict(line)
        column_value = {
            'uid': data['uid'],
            'p_type': Product.MINIK.value,
            't_type': Terminal.Mobile.value,
            'a_type': data['action'],
            'action_time': data['action_time'],
            'location': SocketUtil.ip2int(data['ip']),
            'aimei_object': data['aimei_object'],
            'update_time': -1
        }

        month = DateUtil.now('%Y%m')
        column_value['month'] = month
        column_value['update_time'] = DateUtil.now('%Y-%m-%d %H:%M:%S')

        # 流水需要的

        # 总表需要的
        column_value['provinceid'] = -1
        column_value['isp'] = -1
        column_value['count'] = 1
        column_value['time_span'] = DateUtil.timestamp2date(data['action_time'], '%d%H')
        return column_value

    def insert_many(self, column_values):
        month = DateUtil.now('%Y%m')
        prefix = "INSERT INTO t_data_aimei_user_action_%(month)s (uid, p_type, t_type, a_type, action_time, location, aimei_object, update_time) VALUES "
        prefix = prefix % {'month': month}
        value_fmt = "(%(uid)s, '%(p_type)s', '%(t_type)s', '%(a_type)s', %(action_time)s, %(location)s, '%(aimei_object)s', '%(update_time)s')"
        values = []
        for value in column_values:
            value = value_fmt % value
            values.append(value)
        sql = prefix + ', '.join(values)
        self.db.execute(sql)

    def insert_total_many(self, column_values):
        month = DateUtil.now('%Y%m')
        prefix = "INSERT INTO t_data_aimei_user_action_mob_%(month)s (p_type, a_type, provinceid, isp, time_span, aimei_object, count, update_time) VALUES "
        prefix = prefix % {'month': month}
        value_fmt = "('%(p_type)s', '%(a_type)s', %(provinceid)s, %(isp)s, %(time_span)s, '%(aimei_object)s', %(count)s, '%(update_time)s') "
        end = "ON DUPLICATE KEY UPDATE count = count + 1, update_time = '%(update_time)s'"
        end = end % {'update_time': DateUtil.now('%Y-%m-%d %H:%M:%S')}
        values = []
        for value in column_values:
            value = value_fmt % value
            values.append(value)
        sql = prefix + ', '.join(values) + end
        self.db.execute(sql)

