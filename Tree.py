import json
from Node import Node
from pymongo import MongoClient
from pprint import pprint
class Tree:
	def __init__(self):
		self.client= MongoClient("mongodb://localhost:27017")


	def findNodeByID(self,ID=1,tree="nodes"):
		if tree is "nodes":
			rawNode=self.client.support.nodes.find_one({'_id':int(ID)})
		else:
			print ("ID IS "+ID)
			rawNode=self.client.support.internal.find_one({'_id':int(ID)})
		return Node(rawNode)


	def answer(self,node,response):
		return findNodeByID(node.answer(response))


	def findNodeByTerm(self,terms):
		arrTerms=terms.split(",")
		allNodes={}
		nodeCount={}
		for term in arrTerms:
			nodeList=self.client.support.internal.find({"Tags" : {"$in" : [term.strip().lower()]}})
			for node in nodeList:
				if node["_id"] in nodeCount.keys():
					nodeCount[node["_id"]]+=1
				else: 
					allNodes[node["_id"]]=node
					nodeCount[node["_id"]]=1
		sortedList=sorted(nodeCount, key=nodeCount.__getitem__)
		sortedNodes=[]
		for nodeName in sortedList:
			sortedNodes.append(allNodes[nodeName])
		#rawNode=self.client.support.internal.find_one({'Tag':term})
		return sortedNodes