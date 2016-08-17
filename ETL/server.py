# encoding: utf-8
"""
ETL服务入口
@author Yuriseus
@create 2016-8-17 15:23
"""
import configparser

import settings


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
    from model.user_action import UserAction
    d = {
        'uid': 2,
        'p_type': '0',
        't_type': '1',
        'a_type': '4',
        'aimei_object': '1001',
    }
    user_action = UserAction.gen_model(d)
    user_action.session.add(user_action)
    actions = user_action.Q.all()
    print(actions)
