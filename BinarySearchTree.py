# -*- coding:utf-8 -*-

'''
	一个二叉搜素树的例子，主要包括了插入、删除、查找、前驱、后置、最大值、最小值等功能
'''

'''
	二叉搜索树的节点
'''
class Node(object):

	def __init__(self,key,value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None

	def __str__(self):
		return "key:%s,value:%s ; " % (self.key,self.value) 


class BinarySearchTree(object):

	def __init__(self):
		self.root = None

	# 中序遍历输出二叉树，中序遍历的是value从小到大排序的结果
	def __str__(self):
		return self.inorderTreeWalk(self.root)

	def search(self,value):
		return self.recursionSearch(self.root,value)	

	def recursionSearch(self,x,value):
		if x == None or x.value == value:
			return x
		if value < x.value:
			return self.recursionSearch(x.left,value)
		else:
			return self.recursionSearch(x.right,value)

	def minimum(self,x):
		while x != None:
			x = x.left
		return x

	def maxmum(self,x):
		x = self.root
		while x != None:
			x = x.right
		return x

	# 后置节点
	def successor(self,x):
		if x.right != None:
			return self.minimum(x.right)
		y = x.parent
		while y != None and x == y.right:
			x = y
			y = y.parent
		return y

	# 前驱节点
	def predecessor(self,x):
		if x.left != None:
			return self.maxmum(x.left)
		y = x.parent
		while y != None and x == y.left:
			x = y
			y = y.parent
		return y

	def insert(self,z):
		x = self.root
		y = None
		while x != None:
			y = x
			if z.value < x.value:
				x = x.left
			else:
				x = x.right
		z.parent = y
		if y == None:
			self.root = z
		elif z.value < y.value:
			y.left = z
		else:
			y.right = z

	def transplant(self,u,v):
		if u.parent == None:
			self.root = v
		elif u == u.parent.left:
			u.parent.left = v
		else:
			u.parent.right = v
		if v != None:
			v.parent = u.parent


	def delete(self,z):
		if z.left == None:
			self.transplant(z,z.right)
		elif z.right == None:
			self.transplant(z,z.left)
		elif y == self.minimum(z.right):
			if y.parent != z:
				self.transplant(y,y.right)
				y.right = z.right
				y.right.p = y
			self.transplant(z,y)
			y.left = z.left
			y.left.parent = y

	# 中序遍历
	def inorderTreeWalk(self,x):
		result = ""
		if x != None:
			result += self.inorderTreeWalk(x.left)
			result += str(x)
			result += self.inorderTreeWalk(x.right)
		return result


if __name__ == '__main__':
	tree = BinarySearchTree()
	node1 = Node("d",11)
	node2 = Node("a",1)
	node3 = Node("b",23)
	node4 = Node("t",55)
	node5 = Node("h",22)
	tree.insert(node1)
	tree.insert(node2)
	tree.insert(node3)
	tree.insert(node4)
	tree.insert(node5)
	print(tree)
	print(tree.search(1))
	print(tree.successor(node2))
	print(tree.predecessor(node4))
	tree.delete(node5)
	print(tree)

