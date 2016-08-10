import requests
from flask import jsonify

task_attributes = {}
task_attributes["product"] = "card"
task_attributes["skills"] = "disputes"
task_attributes["phone_number"] = "+14083100604"
task_attributes["customer_name"] = "Badri Krishnan"

worker_state = {}
worker_state["state"] = "Idle"
worker_state["WorkerSid"] = "WKb0f209ebdb42187d919e325af7911807"
#result = requests.post("https://one-route.herokuapp.com/create_task", json=task_attributes)
result = requests.post("https://one-route.herokuapp.com/change_worker_state", json=worker_state)


print result.text
print result
