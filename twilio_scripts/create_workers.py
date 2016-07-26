"""
Create Twilio workers based on TwilioWorkers.csv file
"""
import csv
from twilio.rest import TwilioTaskRouterClient

# Get Twilio client
account_sid = "ACc9111e5c0efc0644b4e754bf2183c1c2"
auth_token  = "86f3177a99d46d4cb6237b106be7bd9c"
workspace_sid = "WSa521ebd8b208fe727465ceb9c92bfc52"
task_router = TwilioTaskRouterClient(account_sid, auth_token)

workerMap = {}

def main():
	# Read CSV and collect workers/attributes
	with open('TwilioWorkers.csv', 'rb') as csv_file:
	    reader = csv.reader(csv_file, delimiter=',', escapechar="\\")
	    for row in reader:
	    	# ignore first row because its just header
	    	if (row[0] != 'Worker Name'):
	        	workerMap[row[0]] = row[1]

	createWorkers()

def createWorkers():
	for worker, skills in workerMap.items():
		twilio_worker = task_router.workers(workspace_sid).create(
		    friendly_name=worker,
		    attributes=skills
		)

		print(twilio_worker.friendly_name + " was added to the workspace with the following attributes: " + skills)

if __name__ == "__main__":
    main()
