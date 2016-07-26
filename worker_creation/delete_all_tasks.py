from twilio.rest import TwilioTaskRouterClient
account_sid = "ACc9111e5c0efc0644b4e754bf2183c1c2"
auth_token  = "86f3177a99d46d4cb6237b106be7bd9c"
workspace_sid = "WSa521ebd8b208fe727465ceb9c92bfc52"
client = TwilioTaskRouterClient(account_sid, auth_token)

for task in client.tasks(workspace_sid).list():
	task.delete()	
	print task.sid + " has been removed from Twilio."
