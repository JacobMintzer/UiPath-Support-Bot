from Node import Node
from pymongo import MongoClient
class Tree:
	def __init__(self):
		self.client= MongoClient("mongodb://localhost:27017")
		
	def getTop(self):
		return "A"

	def findNodeByID(self,ID):
		rawNode=self.client.nodes.find_one({'_id':int(ID)})
		return Node(rawNode)

	def answer(self,node,response):
		return findNodeByID(node.answer(response))