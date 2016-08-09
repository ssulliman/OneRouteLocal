import requests
from flask import jsonify

task_attributes = {}
task_attributes["product"] = "card"
task_attributes["skills"] = "disputes"
task_attributes["phone_number"] = "+14083100604"
task_attributes["customer_name"] = "Badri Krishnan"

result = requests.post("https://one-route.herokuapp.com/create_task", json=task_attributes)

print result.text
print result
