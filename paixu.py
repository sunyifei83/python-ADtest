# -*- coding:utf-8 -*-

from random import randint, shuffle

def _partition(seq, p, r):
    """数组划分，伪码如下：
    PARTITION(A, p, r)
    1  x ← A[r] // 作为划分主元
    2  i ← p-1
    3  for j ← p to r-1
    4    do if A[j] <= x 
    5         then i ← i + 1 // 前划分区域的索引
    6              exchange A[i] ↔A[j] // 小值交换到前面
    7 exchange A[i+1] ↔A[r] // A[r]交换到前区域结尾
    8 return i + 1

    T(n) = θ(n)
    """
    x = seq[r]
    i = p - 1
    for j in range(p, r):
        if seq[j] <= x:
            i += 1
            seq[i], seq[j] = seq[j], seq[i]
    i += 1
    seq[i], seq[r] = seq[r], seq[i]
    return i

def _quick_sort(seq, p, r):
    """递归调用，伪码如下：
    QUICKSORT(A, p, r)
    1  if p < r
    2    then q ← PARTITION(A, p, r)
    3         QUICKSORT(A, p, q-1)
    4         QUICKSORT(A, q+1, r)

    T(n) = θ(n^2)
    """
    if p >= r:
        return
    q = _partition(seq, p, r)
    _quick_sort(seq, p, q - 1)
    _quick_sort(seq, q + 1, r)

def quick_sort(seq):
    """快速排序
    Args:
        seq (Sequence): 一个序列对象。
    """
    _quick_sort(seq, 0, len(seq) - 1)


def _rand_partition(seq, p, r):
    """随机取样交换后再划分，伪码如下：
    RANDOMIZED-PARTITION(A, p, r)
    1  i ← RANDOM(p, r)  // 从A[p..r]中随机选出一个
    2  exchange A[r] ↔ A[i] // A[r]与其交换
    3  return PARTITION(A, p, r)

    T(n) = O(n)
    """
    i = randint(p, r)
    seq[r], seq[i] = seq[i], seq[r]
    return _partition(seq, p, r)

def _rand_qsort(seq, p, r):
    """随机取样划分方式的递归调用，伪码如下：
    RANDOMIZED-QUICKSORT(A, p, r)
    1  if p < r
    2    then q ← RANDOMIZED-PARTITION(A, p, r)
    3         RANDOMIZED-QUICKSORT(A, p, q-1)
    4         RANDOMIZED-QUICKSORT(A, q+1, r)

    T(n) = O(n^2)
    """
    if p >= r:
        return
    q = _rand_partition(seq, p, r)
    _rand_qsort(seq, p, q - 1)
    _rand_qsort(seq, q + 1, r)

def rand_qsort(seq):
    """快速排序（随机化版本）"""
    _rand_qsort(seq, 0, len(seq) - 1)


def qsort(L):
    """快速排序（简易版本）
    更多: Python Cookbook 2nd Edition 第5.11章节
    """
    if not L: return []
    return qsort([x for x in L[1:] if x < L[0]]) + L[0:1] + \
           qsort([x for x in L[1:] if x >= L[0]])

if __name__ == '__main__':
    import timeit

    items = range(10000)
    shuffle(items)

    def test_sorted():
        print(items)
        sorted_items = sorted(items)
        print(sorted_items)

    def test_quick_sort():
        print(items)
        quick_sort(items)
        print(items)

    test_methods = [test_sorted, test_quick_sort] # test_rand_qsort, test_qsort
    for test in test_methods:
        name = test.__name__ # test.func_name
        t = timeit.Timer(name + '()', 'from __main__ import ' + name)
        print(name + ' takes time : %f' % t.timeit(1))