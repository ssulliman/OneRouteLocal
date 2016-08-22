import requests
from flask import jsonify
import json
task_attributes = {}
task_attributes["product"] = "bank"
task_attributes["skills"] = "disputes"
task_attributes["phone_number"] = "+14083100604"
task_attributes["customer_name"] = "Badri Krishnan"

worker_state = {}
worker_state["state"] = "Busy"
worker_state["TaskQueueName"] = "Banking"
worker_state["WorkerSid"] = "WKb0f209ebdb42187d919e325af7911807"
'''result = requests.post("https://one-route.herokuapp.com/create_task", json=task_attributes)
result = requests.post("https://one-route.herokuapp.com/create_task", json=task_attributes)
'''
result = requests.post("https://one-route.herokuapp.com/create_task", json=task_attributes)

#result = requests.post("https://one-route.herokuapp.com/change_worker_state", json=worker_state)r
reservation_resp = requests.get("https://one-route.herokuapp.com/get_worker_reservations", json=worker_state)

#resp = requests.get("https://one-route.herokuapp.com/get_taskqueue_list", json=worker_state)
#task_dict = json.loads(resp.json().get("1"))
#print task_dict["phone_number"]

'''phone_attributes = {}
phone_attributes["to"] = task_dict["phone_number"]
phone_attributes["from"] = "+14082146768"
requests.post("https://one-route.herokuapp.com/make_call", json=phone_attributes)
#print resp.text
'''
