# -*- coding:utf-8 -*-

from enum import Enum
from pymongo import MongoClient
import time

# 获得系统的时间戳 毫秒
currentMilliTime = lambda : int(round(time.time()*1000))

class NodeColor(Enum):
	BLACK = 1
	RED = 2

class Node(object):

	def __init__(self,key,value):
		self.key = key
		self.values = []
		self.values.append(value)
		self.count = 1
		self.left = None
		self.right = None
		self.parent = None
		self.color = None

	def __str__(self):
		return "key:%s,value:%s,left:%s,right:%s,count:%s; " % (self.key,self.values,self.left.key,self.right.key,self.count) 

	def addNewValue(self,value):
		self.values.extend(value)

	def getValueRank(self,value):
		return self.values.index(value) + 1

	def length(self):
		return len(self.values)

class RBTree(object):


	def __init__(self):
		self.nil = Node(-1024,-1024)
		self.nil.count = 0
		self.nil.color = NodeColor.BLACK
		self.root = self.nil

	# 左旋
	def leftRotate(self,x):
		y = x.right
		x.right = y.left
		if y.left != self.nil:
			y.left.parent = x
		y.parent = x.parent
		if x.parent == self.nil:
			self.root = y
		elif x == x.parent.left:
			x.parent.left = y
		else:
			x.parent.right = y
		y.left = x
		x.parent = y
		x.count -= (y.right.count+y.length())
		y.count += (x.left.count+x.length())

	# 右旋
	def rightRotate(self,y):
		x = y.left
		y.left = x.right
		if x.right != self.nil:
			x.right.parent = y
		x.parent = y.parent
		if y.parent == self.nil:
			self.root = x
		elif y == y.parent.left:
			y.parent.left = x
		else:
			y.parent.right = x
		x.right = y
		y.parent = x
		x.count += (y.right.count + y.length())
		y.count -= (x.left.count + x.length())

	def insert(self,z):
		y = self.nil
		x = self.root
		while x != self.nil:
			x.count += 1
			y = x
			if z.key == x.key:
				x.addNewValue(z.values)
				return
			elif z.key < x.key:
				x = x.left
			else:
				x = x.right
		z.parent = y
		if y == self.nil:
			self.root = z
		elif z.key <= y.key:
			y.left = z
		else:
			y.right = z
		z.left = self.nil
		z.right = self.nil
		z.color = NodeColor.RED
		self.insertFixup(z)

	def insertFixup(self,z):
		while z.parent.color == NodeColor.RED:
			if z.parent == z.parent.parent.left:
				y = z.parent.parent.right
				if y.color == NodeColor.RED:
					z.parent.color = NodeColor.BLACK
					y.color = NodeColor.BLACK
					z.parent.parent.color = NodeColor.RED
					z = z.parent.parent
				else:
					if z == z.parent.right:
						z = z.parent
						self.leftRotate(z)		
					z.parent.color = NodeColor.BLACK
					z.parent.parent.color = NodeColor.RED
					self.rightRotate(z.parent.parent)
			else:
				y = z.parent.parent.left
				if y.color == NodeColor.RED:
					z.parent.color = NodeColor.BLACK
					y.color = NodeColor.BLACK
					z.parent.parent.color = NodeColor.RED
					z = z.parent.parent
				else:
					if z == z.parent.left:
						z = z.parent
						self.rightRotate(z)
					z.parent.color = NodeColor.BLACK
					z.parent.parent.color = NodeColor.RED
					self.leftRotate(z.parent.parent)
		self.root.color = NodeColor.BLACK



	# 中序遍历输出二叉树，中序遍历的是value从小到大排序的结果
	def __str__(self):
		return self.inorderTreeWalk(self.root)

	# 中序遍历
	def inorderTreeWalk(self,x):
		result = ""
		if x != self.nil:
			result += self.inorderTreeWalk(x.left)
			result += str(x)
			result += self.inorderTreeWalk(x.right)
		return result

	# 获得节点当前的排名
	def getRank(self,z,value):
		rank = z.getValueRank(value)
		rank += z.right.count
		x = z.parent
		while x != self.nil:
			if z == x.left:
				rank += x.length()
				rank += x.right.count
			x = x.parent
			z = z.parent
		return rank

	def minimum(self,x):
		y = self.nil
		while x != self.nil:
			y = x
			x = x.left
		return y

	def maxmum(self,x):
		y = self.nil
		while x != self.nil:
			y = x
			x = x.right
		return y

	# 后置节点
	def successor(self,x):
		if x.right != self.nil:
			return self.minimum(x.right)
		y = x.parent
		while y != self.nil and x == y.right:
			x = y
			y = y.parent
		return y

	# 前驱节点
	def predecessor(self,x):
		if x.left != self.nil:
			return self.maxmum(x.left)
		y = x.parent
		while y != self.nil and x == y.left:
			x = y
			y = y.parent
		return y

	# 得到排名前N位的value
	def getTopNValues(self,n):
		x = self.maxmum(self.root)
		values = []
		while(n > 0 and x != self.nil):
			values.extend(x.values[0:n])
			n -= len(x.values[0:n])
			x = self.predecessor(x)
		return values

	# 通过key value 得到节点
	def getNodeByKeyAndValue(self,key,value):
		x = self.root
		while x != self.nil and (value not in x.values or key != x.key):
			if key < x.key:
				x = x.left
			else:
				x = x.right
		return None if x == self.nil else x 

	# 以v为根的子树 替换 以u为根的子树 
	def transplant(self,u,v):
		if u.parent == self.nil:
			self.root = v
		elif u == u.parent.left:
			u.parent.left = v
		else:
			u.parent.right = v
		v.parent = u.parent

	
	# 删除节点
	def delete(self,z,value):
		self.nodeCountReduce(z)  #从该节点到根节点路径上的节点count-1
		if z.length() > 1:
			z.values.remove(value)
			return
		y = z
		y.originalColor = y.color
		if z.left == self.nil:
			x = z.right
			self.transplant(z,z.right)
		elif z.right == self.nil:
			x = z.left
			self.transplant(z.z.left)
		else:
			y = self.minimum(z.right)
			y.originalColor = y.color
			x = y.right
			if y.parent == z:
				x.parent = y 
			else:
				self.transplant(y,y.right)
				y.right = z.right
				y.right.parent = y
			self.transplant(z,y)
			y.left = z.left
			y.left.parent = y
			y.color = z.color
			y.count = z.count
		if y.originalColor == NodeColor.BLACK:
			self.deleteFixup(x)

	def nodeCountReduce(self,z):
		while z != self.nil:
			z.count -= 1
			z = z.parent


	def deleteFixup(self,x):
		while x != self.root and x.color == NodeColor.BLACK:
			if x == x.parent.left:
				w = x.parent.right
				if w.color == NodeColor.RED:
					w.color = NodeColor.BLACK
					x.parent.color = NodeColor.RED
					self.leftRotate(x.parent)
					w = x.parent.right
				if w.left.color == NodeColor.BLACK and w.right.color == NodeColor.BLACK:
					w.color = NodeColor.RED
					x = x.parent
				elif w.right.color == NodeColor.BLACK:
					w.left.color == NodeColor.BLACK
					w.color = NodeColor.RED
					self.rightRotate(w)
					w = x.parent.right
				w.color = x.parent.color
				x.parent.color = NodeColor.BLACK
				w.right.color = NodeColor.BLACK
				self.leftRotate(x.parent)
				x = self.root
			else:
				w = x.parent.left
				if w.color == NodeColor.RED:
					w.color = NodeColor.BLACK
					x.parent.color = NodeColor.RED
					self.rightRotate(x.parent)
					w = x.parent.left
				if w.right.color == NodeColor.BLACK and w.left.color == NodeColor.BLACK:
					w.color = NodeColor.RED
					x = x.parent
				elif w.left.color == NodeColor.BLACK:
					w.right.color == NodeColor.BLACK
					w.color = NodeColor.RED
					self.leftRotate(w)
					w = x.parent.left
				w.color = x.parent.color
				x.parent.color = NodeColor.BLACK
				w.left.color = NodeColor.BLACK
				self.rightRotate(x.parent)
				x = self.root
		x.color = NodeColor.BLACK

	def nodeValueIncrease(self,z,value,num):
		self.delete(z,value)
		x = Node(z.key+num,value)
		self.insert(x)



class IntegralRank(object):

	def __init__(self):
		self.tree = RBTree()
		client  = MongoClient(host='localhost',port=27017)
		db = client.Test
		self.UserColl = db.Users
		self.initialize()

	def initialize(self):
		start = currentMilliTime()
		for user in self.UserColl.find():
			node = Node(user.get("integral"),user.get("name"))
			self.tree.insert(node)
		end = currentMilliTime()
		print("初始化所用时间（构建红黑树的时间）：%s" % (end-start))

	def addNewUser(self,name):
		start = currentMilliTime()
		user = self.UserColl.find_one({"name":name})
		if None != user:
			self.UserColl.insert({"name":name,"integral":0})
			self.tree.insert(Node(name,0))
		end = currentMilliTime()
		print("插入用户运行时间：%s" % (end-start))


	def getUserNodeByName(self,name):
		user = self.UserColl.find_one({"name":name})
		if None != user:
			return self.tree.getNodeByKeyAndValue(user.get("integral"),name)
		return None

	def getUserRank(self,name):
		start = currentMilliTime()
		rank = -1
		node = self.getUserNodeByName(name)
		if None != node:
			rank = self.tree.getRank(node,name)
		end = currentMilliTime()
		print("获得用户排名运行时间：%s" % (end-start))
		return rank

	def getTopNUser(self,n):
		start = currentMilliTime()
		topNUsers = self.tree.getTopNValues(n)
		end = currentMilliTime()
		print("获得排名前%s用户运行时间：%s" % (n,end-start))
		return topNUsers

	def userIncreaseIntegral(self,name,num):
		start = currentMilliTime()
		node = self.getUserNodeByName(name)
		if None != node:
			self.UserColl.update({"name":name},{'$inc':{'integral':num}},True,False)
			self.tree.nodeValueIncrease(node,name,num)
		end = currentMilliTime()
		print("用户变更积分运行时间" % (end-start))

	def userDecreaseIntegral(self,name,num):
		self.userIncreaseIntegral(name,-num)

	def deleteUser(self,name):
		start = currentMilliTime()
		node = self.getUserNodeByName(name)
		if None != node:
			self.UserColl.delete_one({"name":name})
			self.tree.delete(node,name)
		end = currentMilliTime()
		print("删除用户运行时间:%s" % (end-start))


if __name__ == '__main__':
	integralRank = IntegralRank()
	while(True):
		n = input("获得排名前多少位的用户：")
		print(integralRank.getTopNUser(int(n)))
		name = input("获得用户的排名：")
		print(integralRank.getUserRank(name))
		delName = input("要删除的用户：")
		integralRank.deleteUser(delName)