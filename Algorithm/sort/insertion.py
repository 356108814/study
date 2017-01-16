# encoding: utf-8
"""
插入排序
1从第一个元素开始，该元素可以认为已经被排序
2取出下一个元素，在已经排序的元素序列中从后向前扫描
3如果该元素（已排序）大于新元素，将该元素移到下一位置
4重复步骤3，直到找到已排序的元素小于或者等于新元素的位置
5将新元素插入到该位置后
6重复步骤2~5
@author Yuriseus
@create 2017-1-16 11:13
"""


def insertion_sort(array):
    length = len(array)
    if length == 1:
        return array
    for i in range(1, length):
        for j in range(i, 0, -1):
            if array[j] < array[j - 1]:
                array[j], array[j - 1] = array[j - 1], array[j]
    return array


if __name__ == '__main__':
    d = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
    print(insertion_sort(d))
