# encoding: utf-8
"""
ETL服务入口
@author Yuriseus
@create 2016-8-17 15:23
"""
import configparser

import settings
from model.user_action import UserAction


def load_conf():
    parser = configparser.RawConfigParser()
    parser.read(settings.DEFAULT_CON_PATH, 'utf-8')
    sections = parser.sections()
    conf = settings.CONF
    for s in sections:
        if s not in conf:
            conf[s] = {}
        items = parser.items(s)
        for item in items:
            conf[s][item[0]] = item[1]

if __name__ == '__main__':
    # 解析配置
    load_conf()
    # TODO 注册服务
    print('ETL service started!')

    user_action = UserAction.model(1)
    actions = user_action.Q.first()
    print(actions)
