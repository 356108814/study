# encoding: utf-8
"""
快速排序
从数列中挑出一个元素作为基准数。
分区过程，将比基准数大的放到右边，小于或等于它的数都放到左边。
再对左右区间递归执行第二步，直至各区间只有一个数。
便于理解：http://blog.csdn.net/morewindows/article/details/6684558
@author Yuriseus
@create 2017-1-16 14:38
"""


def quick_sort(array, left, right):
    # 快速排序，小于基准值的放在左，大于基准值的放在右
    if left >= right:
        return array
    pivot = array[left]    # 基准值
    low = left
    high = right
    while left < right:
        # 先从右向左找小于pivot的数填到基准位置
        while left < right and array[right] >= pivot:
            right -= 1
        array[left] = array[right]
        # 再从左向右找大于基准值填到上次被挖的位置
        while left < right and array[left] <= pivot:
            left += 1
        array[right] = array[left]
    array[left] = pivot    # 当left等于right时，退出。基准值填满最后的坑

    quick_sort(array, low, left - 1)
    quick_sort(array, left + 1, high)
    return array


if __name__ == '__main__':
    d = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
    quick_sort(d, 0, len(d) - 1)
    print(d)
