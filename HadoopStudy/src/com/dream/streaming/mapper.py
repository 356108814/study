#!/usr/local/python3.5.0/bin/python3
# coding: utf-8

import sys


for line in sys.stdin:
    line = line.strip()
    if line.find('STN') == -1:
        year = line[14:18]
        temp = line[26:30]
        print('%s\t%s' % (year, temp))