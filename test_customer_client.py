#!/user/local/bin/python2.7

import requests

task_attributes = {"task_attributes":"value1"}

result = requests.post("https://one-route.herokuapp.com/create_task", data={ "task_attributes": task_attributes })

print result

