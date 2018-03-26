import bot
from Tree import Tree


def _team(event):
	return event["team_id"]
def _user(event):
	if isinstance(event["event"]["user"],str):
		return event["event"]["user"]
	else:
		return event["event"]["user"]["id"]
def _channel(event):
	return event["event"]["channel"]

def i_need_help(bot,event,args=""):
	bot.send_message(_team(event),_user(event),_channel(event),"this is a help message")


def helpm(bot,event,args=""):
	bot.send_message(_team(event),_user(event),_channel(event),"this is a help message",dm=True)

def help(bot,event,args=""):
	bot.sendTreeNode(_team(event),_user(event),_channel(event),dm=True)

def search(bot,event,args=""):
	args=args.replace("search ","")
	print (args)
	if len(args.strip())<1:
		bot.send_message(_team(event),_user(event),_channel(event),"please have a full search term",dm=True)
	else:
		nodeList=bot.tree.findNodeByTerm(args)
		try:
			node=nodeList.pop(0)
		except IndexError:
			node=""
		nodeListString="s"
		for itr in nodeList:
			nodeListString+=(str(itr["_id"])+'_')
		bot.sendSolo(_team(event),_user(event),_channel(event),node,nodeListString,dm=True)