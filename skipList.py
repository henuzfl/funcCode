#-*- coding:utf-8 -*-
import random

'''
	SkipList的工具类
'''

class Node(object):

	def __init__(self,next,key=None,value=None):
		self.key = key
		self.value = value
		self.next = next

	def __eq__(self,obj):
		if obj == None:
			return False
		return self.key == obj.key

class Index(object):

	def __init__(self,node,down,right):
		self.node = node
		self.down = down
		self.right = right

class HeadIndex(Index):

	def __init__(self,node,down,right,level):
		super(HeadIndex,self).__init__(node,down,right)
		self.level = level


class SkipListDict(object):

	def __init__(self):
		self.BASE_HEADER = Node(None)
		self.head = HeadIndex(self.BASE_HEADER,None,None,1)
		self.MAX_LEVEL = 32 #跳表的最大层
		self.p = 0.5 #用来控制生成随机层的是较大值的几率比较大还是较小的几率比较大


	# 插入元素
	def put(self,key,value):
		# 找到在最底层链表中key的前置节点，如果该节点的next不为空并且next.key等于key则更新next.value的值
		b = self.findPredecessor(key)
		if None != b.next and b.next.key == key:
			b.next.value = value
			return
		#新建节点，将节点插入到最底层的链表中
		z = Node(b.next,key,value)
		b.next = z
		#随机生成该节点的索引层级，插入该节点的索引
		self.insertIndex(z,self.randomLevel())


	def insertIndex(self,z,level):
		#如果该节点的层级大于head的层级，那么该层级等于head层级+1，更新头索引
		if level > self.head.level:
			level = self.head.level + 1
			newHead = HeadIndex(self.head.node,self.head,None,level)
			self.head = newHead
		# 新建该节点的索引
		idx = Index(z,None,None)
		for i in range(1,level):
			idx = Index(z,idx,None)
		# 将该节点的索引插入进去
		self.addIndex(idx,level)


	def addIndex(self,idx,idxLevel):
		h = self.head
		level = self.head.level
		# 头索引向下递归，找到与插入索引同等level的索引节点
		for i in range(level - idxLevel):
			h = h.down
		# 头索引从上往下，找到合适的索引建立与该节点索引的连接
		while h != None:
			# 从当前索引向右找到小于且最接近key的索引
			r = h.right
			while r != None:
				if idx.node.key > r.node.key:
					h = r
					r = h.right
					continue
				else:
					break
			# 建立索引连接
			idx.right = r
			h.right = idx
			h = h.down
			idx = idx.down	
		
	# 生成随机层级
	def randomLevel(self):
		v = 1
		while random.random() < self.p and v < self.MAX_LEVEL:
			v += 1
		return v
				

	# 返回小于且最接近key的数据节点，如果不存在就返回最低level的索引头
	def findPredecessor(self,key):
		h = self.head
		while h != None:
			d = h.down
			r = h.right
			while r != None:
				if key > r.node.key:
					h = r 
					r = h.right
					continue
				else:
					break
			if d == None:
				return h.node
			h = d

	# 查找节点
	def get(self,key):
		b = self.findPredecessor(key)
		n = b.next
		if n == None:
			return None
		if key == n.key:
			return n.value
		else:
			return None

	# 删除key
	def remove(self,key):
		h = self.head
		# 从头索引逐层删除该key对应的索引以及节点
		while h != None:
			d = h.down
			r = h.right
			while r != None:
				if key > r.node.key:
					h = r 
					r = h.right
					continue
				else:
					break
			# 在该层找到了key对应的索引，则进行链表删除，如果删除之后是空索引链，则更新跳表的头索引
			if r != None and r.node.key == key:
				h.right = r.right
				if h.node == self.BASE_HEADER and h.right == None:
					self.head = h.down
			# 如果是最底层的索引，则对该节点进行链表删除
			if d == None:
				h.node.next = r.node.next if r != None else None
			h = d

if __name__ == '__main__':
	d = SkipListDict()
	d.put("fsd",1)
	d.put("abc",1)
	d.put("dd",1)
	d.put("ad",1)
	d.put("a",1)
	d.put("bb",1)
	d.put("bba",1)
	d.put("fda",2)
	d.remove("ggggggg")
	print(d.get("fda"))
