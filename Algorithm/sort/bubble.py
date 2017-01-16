# encoding: utf-8
"""
冒泡排序
比较相邻的元素。如果第一个比第二个大，就交换他们两个。
对每一对相邻元素作同样的工作，从开始第一对到结尾的最后一对。这步做完后，最后的元素会是最大的数。
针对所有的元素重复以上的步骤，除了最后一个。
持续每次对越来越少的元素重复上面的步骤，直到没有任何一对数字需要比较。
@author Yuriseus
@create 2017-1-16 10:30
"""


def bubble(array, is_asc=True):
    length = len(array)
    for i in range(length):
        for j in range(0, length - 1):    # 防止j+1越界
            if is_asc:
                if array[j] > array[j + 1]:
                    # 交换
                    array[j], array[j + 1] = array[j + 1], array[j]
            else:
                if array[j] < array[j + 1]:
                    # 交换
                    array[j], array[j + 1] = array[j + 1], array[j]
    return array


# 优化1：某一趟遍历如果没有数据交换，则说明已经排好序了，因此不用再进行迭代了。
# 用一个标记记录这个状态即可。
def bubble_sort2(ary):
    n = len(ary)
    for i in range(n):
        flag = 1                    # 标记
        for j in range(1, n-i):
            if ary[j-1] > ary[j]:
                ary[j-1], ary[j] = ary[j], ary[j-1]
                flag = 0
        if flag:                   # 全排好序了，直接跳出
            break
    return ary


# 优化2：记录某次遍历时最后发生数据交换的位置，这个位置之后的数据显然已经有序了。
# 因此通过记录最后发生数据交换的位置就可以确定下次循环的范围了。
def bubble_sort3(ary):
    n = len(ary)
    k = n                           # k为循环的范围，初始值n
    for i in range(n):
        flag = 1
        for j in range(1, k):        # 只遍历到最后交换的位置即可
            if ary[j-1] > ary[j]:
                ary[j-1], ary[j] = ary[j], ary[j-1]
                k = j               # 记录最后交换的位置
                flag = 0
        if flag:
            break
    return ary


if __name__ == '__main__':
    d = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
    print(bubble(d))
