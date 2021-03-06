# -*- coding: utf-8 -*-
"""
A routing layer for the onboarding bot tutorial built using
[Slack's Events API](https://api.slack.com/events-api) in Python
"""
import json
import bot
import commands
import message
from pprint import pprint
from flask import Flask, request, make_response, render_template

pyBot = bot.Bot()
slack = pyBot.client
global eventList
eventList=[]
app = Flask(__name__)


def process_command(event,bot):
	commandText=str(event["event"]["text"]).replace("!","",1)
	command=commandText.split(" ")[0]
	args=commandText.replace(commandText+" ","",1)
	print ("processing command")
	if hasattr(commands,command):
		print ("has attr")
		cmd=getattr(commands,command)
		cmd(pyBot,event,args)
	else:
		print("no attr")



def _event_handler(event_type, slack_event):
	global eventList
	
	"""
	A helper function that routes events from Slack to our Bot
	by event type and subtype.
	Parameters
	----------
	event_type : str
		type of event recieved from Slack
	slack_event : dict
		JSON response from a Slack reaction event
	Returns
	----------
	obj
		Response object with 200 - ok or 500 - No Event Handler error
	"""
	#pyBot.auth(request.args.get('code'))
	team_id = slack_event["team_id"]
	# ================ Team Join Events =============== #
	# When the user first joins a team, the type of event will be team_join
	if slack_event["event_id"] in eventList:
		print("blocked")
	elif event_type == "team_join":
		print ("Someone joined")
		user_id = slack_event["event"]["user"]["id"]
	# Send the onboarding message
		pyBot.onboarding_message(team_id, user_id)
		return make_response("Welcome Message Sent", 200,)
	# ============== Share Message Events ============= #
	# If the user has shared the onboarding message, the event type will be
	# message. We'll also need to check that this is a message that has been
	# shared by looking into the attachments for "is_shared".
	elif event_type == "message" :
		#pprint(slack_event)
		eventList.append(slack_event["event_id"])
		if len(eventList)>100:
			eventList.pop(0)
		if slack_event["event"]["text"].startswith("!"):
			process_command(slack_event,pyBot)
		else:
			print (slack_event["event"]["text"])
			
		# user_id = slack_event["event"].get("user")
		# #if slack_event["event"]["attachments"][0].get("is_share"):
		# 	# Update the onboarding message and check off "Share this Message"
		# 	#pyBot.update_share(team_id, user_id)
		# print (slack_event)
		# message=""
		# if str(slack_event["event"]["channel"]).startswith('C'):
		# 	print ("this is a public channel")
		# 	if "how do robots work" in str(slack_event["event"]["text"]).lower():
		# 		message="Complete Academy to find out"
		# elif str(slack_event["event"]["channel"]).startswith('D'):
		# 	if "how do robots work" in str(slack_event["event"]["text"]).lower():
		# 		message="its actually magic"
		# 	print ("this is a dm")
		# else:
		# 	print("lol, i dunno, channel is "+str(slack_event["event"]["channel"]))
		# pyBot.send_message(team_id,user_id,message)
		#return make_response("Welcome message updates with shared message",
		#						 200,)

	# ============= Reaction Added Events ============= #
	# If the user has added an emoji reaction to the onboarding message
	elif event_type == "reaction_added":
		user_id = slack_event["event"]["user"]
		# Update the onboarding message
		pyBot.update_emoji(team_id, user_id)
		return make_response("Welcome message updates with reactji", 200,)

	# =============== Pin Added Events ================ #
	# If the user has added an emoji reaction to the onboarding message
	elif event_type == "pin_added":
		user_id = slack_event["event"]["user"]
		# Update the onboarding message
		pyBot.update_pin(team_id, user_id)
		return make_response("Welcome message updates with pin", 200,)

	# ============= Event Type Not Found! ============= #
	# If the event_type does not have a handler
	message = "You have not added an event handler for the %s" % event_type
	# Return a helpful error message
	return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/install", methods=["GET"])
def pre_install():
	"""This route renders the installation page with 'Add to Slack' button."""
	# Since we've set the client ID and scope on our Bot object, we can change
	# them more easily while we're developing our app.
	client_id = pyBot.oauth["client_id"]
	scope = pyBot.oauth["scope"]
	# Our template is using the Jinja templating language to dynamically pass
	# our client id and scope
	return render_template("install.html", client_id=client_id, scope=scope)


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
	"""
	This route is called by Slack after the user installs our app. It will
	exchange the temporary authorization code Slack sends for an OAuth token
	which we'll save on the bot object to use later.
	To let the user know what's happened it will also render a thank you page.
	"""
	# Let's grab that temporary authorization code Slack's sent us from
	# the request's parameters.
	code_arg = request.args.get('code')
	# The bot's auth method to handles exchanging the code for an OAuth token
	pyBot.auth(code_arg)
	return render_template("thanks.html")

@app.route("/ans", methods=["GET", "POST"])
def hearAnswer():
	print ("hearing search response")
	"""
	this is the response that the user will send from the interactive message. 
	This will have the information on the next node, which will be sent to the 
	same location the message came from
	"""
	ans = json.loads(request.form["payload"])
	#pprint(ans)
	#print (type(slack_event))
	#pprint (request.data)
	if ans["actions"][0]["selected_options"][0]["value"].isdigit():
		print("if 1")
		pyBot.sendTreeNode(ans["team"]["id"],ans["user"]["id"],ans["channel"]["id"],node_id=ans["actions"][0]["selected_options"][0]["value"])
	elif ans["actions"][0]["selected_options"][0]["value"].startswith("s"):
		print(ans["actions"][0]["selected_options"][0]["value"])
		nodeList= ans["actions"][0]["selected_options"][0]["value"].replace("s","").split("_")
		print ("num args is "+str(len(nodeList)))
		node=nodeList.pop(0)
		nodeListString="s"+"_".join(nodeList)
		print (len(nodeList))
		#if len(nodeList)<1:
		pyBot.sendSolo(ans["team"]["id"],ans["user"]["id"],ans["channel"]["id"],node,nodeListString,dm=True,)
	else:
		print (ans["actions"][0]["selected_options"][0]["value"])
	return make_response("", 200,)
	#return jsonify(result={"status": 200})

@app.route("/listening", methods=["GET", "POST"])
def hears():
	"""
	This route listens for incoming events from Slack and uses the event
	handler helper function to route events to our Bot.
	"""
	slack_event = json.loads(request.data)
	#print (type(request.data))
	
	# ============= Slack URL Verification ============ #
	# In order to verify the url of our endpoint, Slack will send a challenge
	# token in a request and check for this token in the response our endpoint
	# sends back.
	#       For more info: https://api.slack.com/events/url_verification
	if "challenge" in slack_event:
		return make_response(slack_event["challenge"], 200, {"content_type":
															 "application/json"
															 })

	# ============ Slack Token Verification =========== #
	# We can verify the request is coming from Slack by checking that the
	# verification token in the request matches our app's settings
	if pyBot.verification != slack_event.get("token"):
		message = "Invalid Slack verification token: %s \npyBot has: \
				   %s\n\n" % (slack_event["token"], pyBot.verification)
		# By adding "X-Slack-No-Retry" : 1 to our response headers, we turn off
		# Slack's automatic retries during development.
		make_response(message, 403, {"X-Slack-No-Retry": 1})

	# ====== Process Incoming Events from Slack ======= #
	# If the incoming request is an Event we've subcribed to
	if "event" in slack_event:
		event_type = slack_event["event"]["type"]
		# Then handle the event by event_type and have your bot respond
		return _event_handler(event_type, slack_event)
	# If our bot hears things that are not events we've subscribed to,
	# send a quirky but helpful error response
	return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
						 you're looking for.", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
	app.run(debug=True)