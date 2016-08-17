# encoding: utf-8

import datetime
import uuid
import time
import random

log_path = '/yuri/temp/'


def produce_file_minute():
    """
    每分钟生成一个文件
    """
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M')
        file_path = log_path + now + '.log'
        file_handle = open(file_path, 'w')
        file_handle.write(product_pvs())
        file_handle.flush()
        time.sleep(60)


def product_pvs():
    num = random.randint(10, 100)
    pvs = ''
    for x in range(num):
        pvs += produce_pv()
        time.sleep(0.1)
    return pvs


def produce_add():
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    file_path = log_path + now + '.log'
    file_handle = open(file_path, 'a+')
    while True:
        file_handle.write(produce_pv())
        file_handle.flush()
        time.sleep(1)


def produce_pv():
    """
    格式:ABYH6Y4V4SCV00|2016-03-31 14:00:00|http://www.meda.cc
    :return:
    """
    session_id = str(uuid.uuid1())
    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    url = 'http://www.meda.cc'
    a = [session_id, now_str, url]
    return '|'.join(a) + '\n'


if __name__ == '__main__':
    produce_add()
    produce_file_minute()
    # print product_pvs()
