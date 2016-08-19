# encoding: utf-8
"""
用户行为
@author Yuriseus
@create 2016-8-17 15:14
"""
import time
from ..base import BaseService
from ..enums import Product
from ..enums import Terminal
from ..enums import Action
from model.user_action import UserAction
from util.date import DateUtil


class UserActionService(BaseService):

    def __init__(self):
        self.topics = 'minik_weixin_user_action'
        super().__init__(self.topics)

    def is_need_drop(self, line_data):
        if line_data.find('uid') == -1:
            return True
        return False

    def get_clean_data(self, line_data):
        return line_data

    def process(self, lines):
        # 格式：[I 160815 00:00:00 record_handler:181] timestamp=2016-08-15_00:00:00&action=click_listen_song&songid=2306797&uid=1277909
        for line in lines:
            index = line.find(']')
            line = (line[index+1:]).strip()
            data = self.parser.split_k_v(line)
            column_value = {
                'uid': data['uid'],
                'p_type': Product.MINIK.value,
                't_type': Terminal.Mobile.value,
                'a_type': -1,
                'action_time': -1,
                'location': -1,
                'aimei_object': '',
                'update_time': -1
            }
            action = data['action']
            if action == 'click_listen_song':
                column_value['a_type'] = Action.REQUEST_SONG.value
                column_value['aimei_object'] = data['songid']
            else:
                column_value['a_type'] = Action.CLICK_BUTTON.value
                aimei_object = ''
                if action == 'click_tab':
                    aimei_object = data['tab']
                elif action == 'visit_url':
                    aimei_object = data['url']
                elif action == 'click_play_album':
                    aimei_object = data['albumid']
                column_value['aimei_object'] = aimei_object
            column_value['action_time'] = DateUtil.date2timestamp(data['timestamp'], fmt='%Y-%m-%d_%H:%M:%S')

            # user_action = UserAction.gen_model(column_value)
            # user_action.session.add(user_action)
            # user_action.session.commit()
            self.insert(column_value)
            self.insert_or_update_total(column_value, data)

    def insert(self, column_value, data=None):
        """
        插入流水表
        :param column_value:
        """
        # 设置默认值
        month = DateUtil.now('%Y%m')
        column_value['month'] = month
        column_value['update_time'] = DateUtil.now('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO t_data_aimei_user_action_%(month)s (uid, p_type, t_type, a_type, action_time, location, aimei_object, update_time) VALUES (%(uid)s, '%(p_type)s', '%(t_type)s', '%(a_type)s', %(action_time)s, %(location)s, '%(aimei_object)s', '%(update_time)s')"
        sql %= column_value    # 格式化
        self.db.execute(sql)

    def insert_or_update_total(self, column_value, data=None):
        """
        插入或更新流水总表
        :param column_value:
        """
        # 设置默认值
        month = DateUtil.now('%Y%m')
        column_value['month'] = month
        column_value['provinceid'] = -1
        column_value['isp'] = -1
        column_value['count'] = 1
        column_value['time_span'] = self.get_time_span(data['timestamp'])
        column_value['update_time'] = DateUtil.now('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO t_data_aimei_user_action_mob_%(month)s (p_type, a_type, provinceid, isp, time_span, aimei_object, count, update_time) VALUES ('%(p_type)s', '%(a_type)s', %(provinceid)s, %(isp)s, %(time_span)s, '%(aimei_object)s', %(count)s, '%(update_time)s') ON DUPLICATE KEY UPDATE count = count + 1, update_time = '%(update_time)s'"
        sql %= column_value    # 格式化
        self.db.execute(sql)

    def get_time_span(self, date_str):
        # 2016-08-15_23:59:59
        time_span = date_str[8:10] + date_str[11:13]
        return int(time_span)
