#!/user/local/bin/python2.7

import requests

task_values="{\"key1\":\"value1\", \"key2\":\"value2\"}"

task_attributes = {"task_attributes":task_values}

result = requests.post("https://one-route.herokuapp.com/create_task", json=task_attributes)

print result.text

print result

