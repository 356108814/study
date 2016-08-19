# encoding: utf-8
"""
公共枚举
@author Yuriseus
@create 2016-8-18 22:57
"""

from enum import Enum


class Product(Enum):
    MINIK = 0
    KSHOW = 1


class Terminal(Enum):
    MACHINE = 0    # 实体机
    Mobile = 1


class Action(Enum):
    REQUEST_SONG = 0    # 点播歌曲
    LOGIN = 1
    LOGOUT = 2
    CONSUME = 3
    CLICK_BUTTON = 4
    VIEW_SONG = 5       # 查看歌曲
