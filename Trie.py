#-*-coding:utf-8-*-
'''
   Trie树的例子
'''
from collections import deque
import re
from MinHeap import MinHeap




# Trie树的节点
class Node:

    def __init__(self):
        self.value = None
        # 节点的子节点
        self.children = set()
        # 插入的单词经过这个字符的个数，用来统计以这个字符为前缀的数量
        self.count = 0
        # 加入为单词节点，插入的这个单词的数量
        self.wordCount = 0


# Trie树
class Trie:

    def __init__(self):
        self.root = Node()
        self.n = 5 # 返回以key为前缀出现次数前n多的单词

    # 插入操作
    def insert(self, key):
        node = self.root
        for a in key:
            isFound = False
            # 没经过一个节点，这个节点count+1，然后跳到下一层；如果是单词的最后一个节点，则wordCount+1，跳出循环
            for subNode in node.children:
                if subNode.value == a:
                    subNode.count += 1
                    if a == key[len(key)-1]:
                        subNode.wordCount += 1
                    isFound = True
                    node = subNode
                    break
            # 如果没有找到这个字符，则新加入这个字符节点
            if not isFound:
                temp = Node()
                temp.value = a
                temp.count = 1
                if a == key[len(key)-1]:
                    temp.wordCount = 1
                node.children.add(temp)
                node = temp


    '''
        查询单词是否在Trie树中
    '''

    def search(self, key):
        node = self.root
        (exists, node) = self.searchNode(key)
        if exists:
            print("以%s为前缀的单词数量为：%d" % (key, node.count))
            self.countResult(key, node)
        else:
            print("以%s为前缀的单词数量为：%d" % (key, 0))


    '''
        查找节点
        返回结果：
                是否存在
                最后一个字符的节点
    '''

    def searchNode(self, key):
        node = self.root
        for a in key:
            isFound = False
            for subNode in node.children:
                if subNode.value == a:
                    node = subNode
                    isFound = True
                    break
            if not isFound:
                return False, None
        return True, node


    '''
        获得最后统计的结果，包含以key为前缀的单词出现次数最多的前n个
    '''

    def countResult(self, key, node):
        # 使用最小堆来实现topK问题
        minHeap = MinHeap(self.n)
        self.nodeInsertMinHeap(minHeap,key[:len(key)-1],node)
        # 按照单词出现次数由大到小对最小堆进行排序
        minHeap.heapSort()
        # 输出最小堆的结果
        minHeap.display()

    '''
        递归的找到所有以key为前缀的单词，并插入到最小堆
    '''
    def nodeInsertMinHeap(self,minHeap,key,node):
        key += node.value
        if node.wordCount > 0:
            minHeap.minHeapInsert(key, node.wordCount)
        for temp in node.children:
            self.nodeInsertMinHeap(minHeap,key, temp)

    

    '''
        广搜输出整条树
    '''

    def display(self):
        q = deque()
        q.appendleft(self.root)
        print(len(q))
        while len(q) != 0:
            node = q.pop()
            if node.value != None:
                print(node.value + "  "+str(node.count))
            for temp in node.children:
                q.appendleft(temp)


'''
    读取path路径中的文本，并提取其中出现的单词
'''


# 简易的获得英文文档的全部单词
def words(path):
    with open(path, 'r') as f:
        str = f.read()
        return re.findall('[a-z]+', str.lower())

if __name__ == '__main__':
    trie = Trie()
    # 使用全本的福尔摩斯作为英文文本输入
    words = words("C:\\testData\\Sherlock.txt")
    for word in words:
        trie.insert(word)
    trie.search('she')