# encoding: utf-8
"""
服务器管理
@author Yuriseus
@create 2016-8-17 15:49
"""
import os

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

    def process_interval(self):
        """
        定时处理
        :return:
        """
        for k, service in self._running_services.items():
            service.instance.check_process()
            service.instance.check_batch_process()

    def register(self, service):
        """
        服务注册
        :param service: Service对象
        :return:
        """
        service_new = copy.copy(service)
        service_cls = self.import_object(service.path)
        if service_cls:
            if service.is_from_dir:
                service_instance = service_cls(service.dir_path)
            else:
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

    def check_config(self):
        """
        服务检测，通过定时读取配置文件
        :return:
        """
        service_conf_dict = settings.CONF['service']
        for k, v in service_conf_dict.items():
            if k == 'base_dir':
                continue
            service = Service()
            service.name = k
            va = v.split(',')
            if len(va) != 4:
                logger.error('服务配置错误：%s' % str(service))
                continue
            service.path = va[0]
            if va[1].isdigit():
                service.version = int(va[1])
            else:
                logger.error('服务版本号配置错误，期望是数字，而配置的是：%s' % va[1])
                continue
            if va[2] in ['0', '1']:
                service.is_start = int(va[2])
            else:
                logger.error('服务是否启动配置错误，只能为0或1')
                continue
            if va[3] in ['0', '1']:
                service.is_from_dir = int(va[3])
                if service.is_from_dir:
                    base_dir = settings.CONF['service']['base_dir']
                    dir_path = os.path.join(base_dir, service.name)
                    service.dir_path = dir_path
                    if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
                        logger.error('服务%s：对应的数据文件夹文件夹不存在：%s' % (str(service), service.dir_path))
                        continue
            else:
                logger.error('服务数据源是否为文件夹配置错误，只能为0或1')
                continue
            uuid = service.path    # 服务唯一标识
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
            logger.error("服务类不存在：%s" % name)
            return None





