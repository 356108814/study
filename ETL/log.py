# encoding: utf-8
"""
增加多文件日志支持
@author Yuriseus
@create 2016-8-3 19:15
"""
import logging
import logging.handlers


def gen_channel(filename):
    return logging.handlers.TimedRotatingFileHandler(
            filename='log/%s.log' % filename,
            when='midnight',
            interval=1,
            backupCount=3)


class LogFormatter(logging.Formatter):
    DEFAULT_FORMAT = '%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'
    DEFAULT_DATE_FORMAT = '%y%m%d %H:%M:%S'
    DEFAULT_COLORS = {
        logging.DEBUG: 4,  # Blue
        logging.INFO: 2,  # Green
        logging.WARNING: 3,  # Yellow
        logging.ERROR: 1,  # Red
    }

    def __init__(self, color=True, fmt=DEFAULT_FORMAT,
                 datefmt=DEFAULT_DATE_FORMAT, colors=DEFAULT_COLORS):
        logging.Formatter.__init__(self, fmt, datefmt=datefmt)


class Logger(object):

    def __init__(self):
        self._loggers = {}

    def info(self, msg, name=None):
        """
        记录日志
        :param msg:
        :param name: 日志文件名称，如不存在，则创建
        :return:
        """
        if not name:
            name = 'ETL'
        if name not in self._loggers:
            temp_logger = logging.getLogger(name)
            channel = gen_channel(name)
            channel.setFormatter(LogFormatter(color=True))
            temp_logger.addHandler(channel)
            self._loggers[name] = temp_logger
        current_logger = self._loggers[name]
        current_logger.info(msg)


logger = Logger()
