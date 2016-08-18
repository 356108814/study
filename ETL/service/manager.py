# encoding: utf-8
"""
服务器管理
@author Yuriseus
@create 2016-8-17 15:49
"""
import settings
import copy
from .service import Service
from log import logger


class ServiceManager(object):
    def __init__(self):
        # 当前已运行的服务，键为服务path，值为Service对象
        self._running_services = {}

    @staticmethod
    def instance():
        if not hasattr(ServiceManager, "_instance"):
            ServiceManager._instance = ServiceManager()
        return ServiceManager._instance

    def check_all_process(self):
        """
        按时间窗口检测处理数据
        :return:
        """
        for k, service in self._running_services.items():
            service.instance.check_process()

    def register(self, service):
        """
        服务注册
        :param service: Service对象
        :return:
        """
        service_new = copy.copy(service)
        service_cls = self.import_object(service.path)
        if service_cls:
            service_instance = service_cls()
            service_new.instance = service_instance
            logger.info('服务注册成功：%s' % str(service))
            self._running_services[service.path] = service_new
            service_instance.start()

    def unregister(self, service):
        """
        服务取消注册
        :param service: Service对象
        :return:
        """
        if service and service.instance:
            service_instance = service.instance
            service_instance.stop()
            del self._running_services[service.path]
            logger.info('服务取消注册成功：%s' % str(service))
            service = None

    def check(self):
        """
        服务检测，通过定时读取配置文件
        :return:
        """
        service_conf_dict = settings.CONF['service']
        for k, v in service_conf_dict.items():
            service = Service()
            service.name = k
            va = v.split(',')
            if len(va) != 3:
                logger.warning('服务配置错误：%s' % str(service))
                continue
            service.path = va[0]
            service.version = int(va[1])
            service.is_start = int(va[2])
            uuid = service.path    # 服务器唯一标识
            if uuid in self._running_services:
                running_service = self._running_services[uuid]
                if service != running_service:    # 服务已改变
                    self.unregister(running_service)
                    if service.is_start:
                        self.register(service)
            else:    # 新增服务
                if service.is_start:
                    self.register(service)

    def import_object(self, name):
        if not isinstance(name, str):
            name = name.encode('utf-8')
        if name.count('.') == 0:
            return __import__(name, None, None)

        parts = name.split('.')
        obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
        try:
            return getattr(obj, parts[-1])
        except AttributeError:
            logger.error("No module named %s" % parts[-1])
            return None





