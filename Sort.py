
import random as random
import sys
import numpy as np
sys.setrecursionlimit(1000000)  # 设置python的递归深度

'''
    常见的排序算法
'''

randArr = []
i = 0
while i < 10:
    randArr.append(random.randint(1, 100))
    i += 1

# print(randArr)


def exchange(arr, i, j):
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp

#########################################################
'''
    快速排序
'''


def quickSort(arr, p, r):
    if p < r:
        q = partition(arr, p, r)
        quickSort(arr, p, q-1)
        quickSort(arr, q+1, r)


def partition(arr, p, r):
    key = arr[r]
    i = p - 1
    j = p
    while j < r:
        if arr[j] >= key:
            j += 1
        else:
            i += 1
            exchange(arr, i, j)
            j += 1
    exchange(arr, i+1, r)
    return i+1


#########################################################
'''
    计数排序
'''


def countSort(arr):
    count = [0] * 10001
    for i in randArr:
        count[i] += 1
    j = 0
    re = []
    while j < len(count):
        for i in range(count[j]):
            re.append(j)
        j += 1

#########################################################
'''
    归并排序
'''


def mergeSort(arr, p, r):
    if p < r:
        q = p+(int)((r-p)/2)
        mergeSort(arr, p, q)
        mergeSort(arr, q+1, r)
        merge(arr, p, q, r)


def merge(arr, p, q, r):
    lArr = arr[p:q+1]
    rArr = arr[q+1:r+1]
    lArr.append(sys.maxsize)
    rArr.append(sys.maxsize)
    i = 0
    j = 0
    k = p
    while k <= r:
        if lArr[i] <= rArr[j]:
            arr[k] = lArr[i]
            i += 1
        else:
            arr[k] = rArr[j]
            j += 1
        k += 1

#########################################################
'''
    冒泡排序
'''


def bublleSort(arr):
    i = len(arr) - 1
    while i > 0:
        j = 0
        while j < i:
            if arr[j] > arr[j+1]:
                exchange(arr, j, j+1)
            j += 1
        i -= 1

#########################################################
'''
    鸡尾酒排序,冒泡排序的变种
'''


def cocktailSort(arr):
    i = len(arr) - 1
    k = 0
    while k < i:
        j = k
        while j < i:
            if arr[j] > arr[j+1]:
                exchange(arr, j, j+1)
            j += 1
        j -= 1
        while j > k:
            if arr[j] < arr[j - 1]:
                exchange(arr, j-1, j)
            j -= 1
        k += 1
        i -= 1
#########################################################
'''
    插入排序
'''


def insertSort(arr):
    i = 1
    while i < len(arr):
        key = arr[i]
        j = i - 1
        while j >= 0:
            if arr[j] > key:
                arr[j+1] = arr[j]
            else:
                break
            j -= 1
        arr[j+1] = key
        i += 1

#########################################################
'''
    shell排序
'''


def shellSort(arr):
    n = len(arr)
    h = 1
    while h <= (int)(n/9):
        h = h * 3 + 1
    while h > 0:
        i = h
        while i < n:
            temp = arr[i]
            j = i - h
            while j >= 0 and arr[j] > temp:
                arr[j+h] = arr[j]
                j -= h
            arr[j+h] = temp
            i += 1
        h = (int)(h / 3)

#########################################################
'''
    堆排序
'''


class MaxHeap():

    def __init__(self, arr):
        self.queue = arr
        self.heapSize = len(self.queue)
        self.bulidMaxHeap()

    def parent(self, i):
        return (int)((i-1)/2)

    def left(self, i):
        return (i*2) + 1

    def right(self, i):
        return (i*2) + 2

    def exchange(self, i, j):
        temp = self.queue[i]
        self.queue[i] = self.queue[j]
        self.queue[j] = temp

    def maxHeapify(self, i):
        l = self.left(i)
        r = self.right(i)
        largest = i
        if l < self.heapSize and self.queue[largest] < self.queue[l]:
            largest = l
        if r < self.heapSize and self.queue[largest] < self.queue[r]:
            largest = r
        if largest != i:
            self.exchange(largest, i)
            self.maxHeapify(largest)

    def bulidMaxHeap(self):
        i = (int)(self.heapSize / 2)
        while i >= 0:
            self.maxHeapify(i)
            i -= 1

    def heapSort(self):
        i = self.heapSize - 1
        while i > 0:
            self.exchange(i, 0)
            self.heapSize -= 1
            self.maxHeapify(0)
            i -= 1


def heapSort(arr):
    maxHeap = MaxHeap(arr)
    maxHeap.heapSort()

#########################################################
'''
    选择排序
'''


def selectSort(arr):
    i = 0
    while i < len(arr):
        j = i + 1
        min = arr[i]
        index = i
        while j < len(arr):
            if min > arr[j]:
                min = arr[j]
                index = j
            j += 1
        exchange(arr, i, index)
        i += 1
    print(arr)
'''
    桶排序
'''

def getMinAndMax(arr):
    min = 2 << 40
    max = - 2 << 40
    for a in arr:
        if a < min:
            min = a
        if a > max:
            max = a
    return min,max

def bucketSort(arr):
    min,max = getMinAndMax(arr)
    buckets = np.zeros(max - min + 1)
    for a in arr:
        buckets[a - min] += 1
    result = []
    for i in range(int(buckets.size)):
        for j in range(int(buckets[i])):
            result.append(i+min)
    return result


randArr.sort()
if __name__ == '__main__':
    print(bucketSort(randArr))
# countSort(randArr)
# quickSort(randArr, 0, len(randArr)-1)
# mergeSort(randArr, 0, len(randArr)-1)
# bublleSort(randArr)
# cocktailSort(randArr)
# insertSort(randArr)
# selectSort(randArr)
# shellSort(randArr)
# heapSort(randArr)
# print(randArr)
