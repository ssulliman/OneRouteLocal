import requests

task_attributes="{\"product\":\"card\",\"skills\":\"[\"disputes\"]\"}"

result = requests.post("https://one-route.herokuapp.com/create_task", json=task_attributes)

print result.text
print result
