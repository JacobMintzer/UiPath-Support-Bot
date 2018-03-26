import json
from pprint import pprint

class Node:

	def __init__(self,data):
		print("AAA")
		pprint(data)
		self.content=data["Content"]
		self.IDRef=data["_id"]
		if "Type" in data.keys():
			self.type="Solo"
		else:
			self.type="tree"
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
		
		data=json.load(open("interactiveMessage.json","r"))
		data["text"]=self.content
		if self.type=="Solo":
			data["attachments"][0]["text"]="Does this answer your question?"
			#data["attachments"][0]["actions"][0]["type"]="button"
			data["attachments"][0]["actions"][0]["options"]=[]
			data["attachments"][0]["actions"][0]["options"].append({"text":"Yes","value":""})
		else:
			if len(self.children)<1:
				data["attachments"]=[{}]
			else:
				data["attachments"][0]["text"]=self.question
				data["attachments"][0]["actions"][0]["options"]=[]
				for (answerText, answerContent) in zip(self.answers,self.children):
					data["attachments"][0]["actions"][0]["options"].append({"text":answerText,"value":answerContent})

		response=json.dumps(data)
		return data
