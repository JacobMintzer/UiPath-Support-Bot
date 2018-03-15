import json

class Node:

	def __init__(self,data):
		self.content=data["Content"]
		self.IDRef=data["_id"]
		self.children=data["Children"]
		self.parent=data["Parent"]
		self.question=data["Question"]
		self.answers=data["Answers"]


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

	def getMessage(self):
		data=json.load(open("interactiveMessage.json","r").read())
		data["text"]=self.content
		if len(self.children)<1:
			data["attachments"]=[{}]
		else:
			data["attachments"][0]["text"]=self.question
			data["attachments"][0]["actions"][0]["options"]=[]
			for (answerText, answerContent) in zip(self.answers,self.children):
				data["attachments"][0]["actions"][0]["options"].append({"text":answerText,"value":answerContent})
		response=json.dumps(data)
		return response
