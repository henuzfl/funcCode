#-*-coding:utf-8-*-
'''
   指定大小的最小堆例子,用来解决topK问题
'''
import sys


class Node:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class MinHeap:

    def __init__(self, maxSize=sys.maxsize):
        self.queue = []
        self.heapSize = 0
        self.maxSize = maxSize

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

    def heapIncreseKey(self, i, node):
        if node.value < self.queue[i].value:
            return "error"
        else:
            self.queue[i] = node
            while (i > 0) and (self.queue[self.parent(i)].value > self.queue[i].value):
                self.exchange(self.parent(i), i)
                i = self.parent(i)

    def minHeapInsert(self, key, value):
        node = Node(key, value)
        if self.heapSize < self.maxSize:
            self.heapSize += 1
            self.queue.append(Node("-1", -1))
            self.heapIncreseKey(self.heapSize-1, node)
        else:
            if node.value > self.queue[0].value:
                self.queue[0] = node
                self.minHeapify(0)

    def minHeapInsertNode(self, node):
        if self.heapSize < self.maxSize:
            self.heapSize += 1
            if self.heapSize > len(self.queue):
                self.queue.append(node)
            else:
                self.queue[self.heapSize-1] = node
            self.heapIncreseKey(self.heapSize-1, node)
        else:
            if node.value > self.queue[0].value:
                self.queue[0] = node
                self.minHeapify(0)

    def minHeapify(self, i):
        l = self.left(i)
        r = self.right(i)
        minimal = i
        if l < self.heapSize and self.queue[l].value < self.queue[minimal].value:
            minimal = l
        if r < self.heapSize and self.queue[r].value < self.queue[minimal].value:
            minimal = r
        if minimal != i:
            self.exchange(i, minimal)
            self.minHeapify(minimal)

    def clear(self):
        self.queue.clear()

    def heapSort(self):
        i = len(self.queue)-1
        while i >= 0:
            self.exchange(0, i)
            self.heapSize -= 1
            self.minHeapify(0)
            i -= 1

    def extractMin(self):
        if self.heapSize <= 0:
            return None
        else:
            result = self.queue[0]
            self.queue[0] = self.queue[self.heapSize-1]
            self.queue[self.heapSize-1] = Node
            self.heapSize -= 1
            self.minHeapify(0)
            return result

    def display(self):
        for a in range(len(self.queue)):
            if self.queue[a].key == None:
                print("None"+":"+str(self.queue[a].value))
            else:
                print(self.queue[a].key+"  "+str(self.queue[a].value))

if __name__ == '__main__':
    minHeap = MinHeap()
    minHeap.minHeapInsertNode(Node("a", 22))
    minHeap.minHeapInsertNode(Node("b", 10))
    minHeap.minHeapInsertNode(Node("c", 33))
    minHeap.minHeapInsertNode(Node("d", 55))
    minHeap.minHeapInsertNode(Node("e", 12))
    minHeap.minHeapInsertNode(Node("f", 4))
    minHeap.minHeapInsertNode(Node("g", 66))
    minHeap.minHeapInsertNode(Node("q", 3))
    minHeap.heapSort()
    minHeap.minHeapInsertNode(Node("l", 44))
    minHeap.display()
