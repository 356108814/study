# encoding: utf-8
"""
选择排序
首先在未排序序列中找到最小（大）元素，存放到排序序列的起始位置
然后，再从剩余未排序元素中继续寻找最小（大）元素
然后放到已排序序列的末尾。以此类推，直到所有元素均排序完毕
@author Yuriseus
@create 2017-1-16 11:13
"""


def select_sort(array):
    length = len(array)
    for i in range(length):
        min_idx = i    # 最小值下标
        for j in range(i + 1, length):
            if array[j] < array[min_idx]:
                min_idx = j
        # 交换最小值，最小值移到左边
        array[i], array[min_idx] = array[min_idx], array[i]
    return array


if __name__ == '__main__':
    d = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
    print(select_sort(d))
