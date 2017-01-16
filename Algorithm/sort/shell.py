# encoding: utf-8
"""
希尔排序
也称递减增量排序算法，是插入排序的一种更高效的改进版本。希尔排序是非稳定排序算法
@author Yuriseus
@create 2017-1-16 14:13
"""


def shell_sort(array):
    length = len(array)
    # 初始步长
    gap = round(length/2)
    while gap > 0:
        for i in range(gap, length):
            # 每个步长进行插入排序
            temp = array[i]
            j = i
            # 插入排序
            while j >= gap and array[j - gap] > temp:
                array[j] = array[j - gap]
                j -= gap
            array[j] = temp
        # 新的步长
        gap = round(gap / 2)
    return array


if __name__ == '__main__':
    d = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
    print(shell_sort(d))
