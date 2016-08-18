# encoding: utf-8
"""
ETL服务入口
@author Yuriseus
@create 2016-8-17 15:23
"""
import configparser
import time
import threading
import settings
from service.manager import ServiceManager
from log import logger


class Server(object):
    def __init__(self):
        self._serviceManager = None
        self._check_conf_interval = 10    # 秒

    def load_conf(self):
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

    def start(self):
        logger.info(u'加载解析配置：%s' % settings.DEFAULT_CON_PATH)
        self.load_conf()
        logger.info(u'服务初始化')
        self._serviceManager = ServiceManager.instance()
        logger.info(u'服务启动完成，进入主循环')

        # 主循环
        conf_flag = 0
        while True:
            time.sleep(1)
            conf_flag += 1
            if conf_flag >= self._check_conf_interval:
                self.load_conf()
                self._serviceManager.check()
                conf_flag = 0

            # 每秒检测
            self._serviceManager.check_all_process()




if __name__ == '__main__':
    server = Server()
    server.start()


    # from model.user_action import UserAction
    # d = {
    #     'uid': 2,
    #     'p_type': '0',
    #     't_type': '1',
    #     'a_type': '4',
    #     'aimei_object': '1001',
    # }
    # user_action = UserAction.gen_model(d)
    # user_action.session.add(user_action)
    # actions = user_action.Q.all()
    # print(actions)
