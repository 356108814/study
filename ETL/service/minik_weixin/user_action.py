# encoding: utf-8
"""
用户行为
@author Yuriseus
@create 2016-8-17 15:14
"""
from ..base import BaseService


class UserActionService(BaseService):

    def __init__(self):
        self.topics = 'minik_weixin_user_action'
        super().__init__(self.topics)

    def process(self, lines):
        # 格式：timestamp=2016-08-15_00:00:00&action=click_listen_song&songid=2306797&uid=1277909
        for line in lines:
            data = self.parser.split_k_v(line)
