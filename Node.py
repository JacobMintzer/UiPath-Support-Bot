import json

class Node:

	def __init__(self,data):
		self.content=data["content"]
		self.IDRef=data["IDRef"]
		self.children=data["children"]
		self.parent=data["parent"]
		self.question=data["question"]


	def answer(self,response):
		return children[response]

	def getContent(self):
		return self.content

	def getIDRef(self):
		return self.IDRef

	def getChildren(self):
		return self.children

	def getParent(self):
		return self.parent

	def getQuestion(self):
		return self.question