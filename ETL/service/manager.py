# encoding: utf-8
"""
服务器管理
@author Yuriseus
@create 2016-8-17 15:49
"""


class ServiceManager(object):
    def __init__(self):
        self._services = []

    @staticmethod
    def instance():
        if not hasattr(ServiceManager, "_instance"):
            ServiceManager._instance = ServiceManager()
        return ServiceManager._instance

    def register(self, service_name):
        pass

    def unregister(self, service_name):
        pass

