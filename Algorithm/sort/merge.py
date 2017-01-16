# encoding: utf-8
"""
归并排序
迭代法
申请空间，使其大小为两个已经排序序列之和，该空间用来存放合并后的序列
设定两个指针，最初位置分别为两个已经排序序列的起始位置
比较两个指针所指向的元素，选择相对小的元素放入到合并空间，并移动指针到下一位置
重复步骤3直到某一指针到达序列尾
将另一序列剩下的所有元素直接复制到合并序列尾

递归法
原理如下（假设序列共有n个元素）：
将序列每相邻两个数字进行归并操作，形成 {\displaystyle floor(n/2)} floor(n/2)个序列，排序后每个序列包含两个元素
将上述序列再次归并，形成 {\displaystyle floor(n/4)} floor(n/4)个序列，每个序列包含四个元素
重复步骤2，直到所有元素排序完毕
@author Yuriseus
@create 2017-1-16 14:38
"""
from collections import deque


def merge(left, right):
    merged, left, right = deque(), deque(left), deque(right)
    while left and right:
        if left[0] <= right[0]:
            merged.append(left.popleft())
        else:
            merged.append(right.popleft())
    merged.extend(right if right else left)
    return list(merged)


def merge_sort(array):
    if len(array) <= 1:
        return array
    middle = int(len(array) // 2)
    left = merge_sort(array[:middle])
    right = merge_sort(array[middle:])
    return merge(left, right)


if __name__ == '__main__':
    d = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
    print(merge_sort(d))
