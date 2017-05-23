# -*- coding:utf-8 -*-

from pymongo import MongoClient

import time

# 获得系统的时间戳 毫秒
currentMilliTime = lambda : int(round(time.time()*1000))

'''
	用户类，比较简单，只有两个字段name--姓名，integral--积分
'''
# 积分的最大值
maxIntegral = 50000


class IntegralRank(object):

	def __init__(self):
		client  = MongoClient(host='localhost',port=27017)
		db = client.Test
		self.UserColl = db.Users

	def insertUser(self,name,integral):
		if None == self.UserColl.find_one({"name":name}):
			self.UserColl.insert({"name":name,"integral":integral})


	def getUserRank(self,name):
		start = currentMilliTime()
		user = self.UserColl.find_one({"name":name})
		rank = 0
		for userObj in self.UserColl.find({"integral":user.get("integral")}):
			rank += 1
			if name == userObj.get("name"):
				break
		rank += self.UserColl.count({"integral":{"$gt":user.get("integral")}})
		end = currentMilliTime()
		print("获得用户排名运行时间：%s" % (end-start))
		return rank

	def getTopNUsers(self,n):
		start = currentMilliTime()
		topNUsers = []
		for u in self.UserColl.find({},{"name":1}).limit(n).sort("integral",-1):
			topNUsers.append(u.get("name"))
		end = currentMilliTime()
		print("获得排名前%s用户运行时间：%s" % (n,end-start))
		return topNUsers

	def dataInputDB(self):
		n = 1000000
		global maxIntegral
		'''
			为了最大程度的模拟真实环境，根据2/8原则，有百分之二十的人在百分之八十的高分区，有百分之八十的人在百分之二十低分区
		'''
		for i in range(n):
			print(i)
			integral = random.randint(int(maxIntegral*0.8),maxIntegral) if random.random() > 0.8 else random.randint(0,int(maxIntegral*0.2))
			user = User(self.getRandomUserName(),integral)
			self.insertUser(user)
		

	def getRandomUserName(self):
		nameChar = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
		nameLen = random.randint(4,12)
		name = ""
		while nameLen > 0:
			name += random.choice(nameChar)
			nameLen -= 1
		return name

if __name__ == '__main__':
	integralRank = IntegralRank()
	while(True):
		n = input("获得排名前多少位的用户：")
		print(integralRank.getTopNUsers(int(n)))
		name = input("获得用户的排名：")
		print(integralRank.getUserRank(name))