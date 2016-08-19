# encoding: utf-8
"""
用户行为
@author Yuriseus
@create 2016-8-17 15:14
"""
from ..base import BaseService
from ..enums import Product
from ..enums import Terminal
from ..enums import Action
from model.user_action import UserAction


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
                'aimei_object': ''
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

            user_action = UserAction.gen_model(column_value)
            user_action.session.add(user_action)
            user_action.session.commit()
