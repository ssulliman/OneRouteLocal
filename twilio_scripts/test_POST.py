import requests
from flask import jsonify

task_attributes = {}
task_attributes["product"] = "card"
task_attributes["skills"] = "disputes"

result = requests.post("https://one-route.herokuapp.com/create_task", json=task_attributes)

print result.text
print result
