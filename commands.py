import bot

def _team(event):
	return event["team_id"]
def _user(event):
	if isinstance(event["event"]["user"],str):
		return event["event"]["user"]
	else:
		return event["event"]["user"]["id"]
def _channel(event):
	return event["event"]["channel"]

def help(bot,event,args=""):
	bot.send_message(_team(event),_user(event),_channel(event),"this is a help message")


def helpm(bot,event,args=""):
	bot.send_message(_team(event),_user(event),_channel(event),"this is a help message",dm=True)

def interactive(bot,event):
	bot.sendInteractive(_team(event),_user(event),_channel(event),"this is a help message")