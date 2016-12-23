#!/usr/local/python3.5.0/bin/python3
# coding: utf-8

import sys

year = None
max = 0

for line in sys.stdin:
    (year, temp) = line.split('\t')
    temp = float(temp)
    if temp > max:
        max = temp
print('%s\t%s' % (year, max))
