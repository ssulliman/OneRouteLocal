"""
Generate a token that lasts 1000 days for a given worker_sid
Parameters
----------
worker_sid
"""
import argparse
from twilio import jwt
from twilio.task_router import TaskRouterWorkerCapability

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('worker_sid', help='<worker_sid>')
args = parser.parse_args()

#OneRoute Account Credentials
account_sid = "ACc9111e5c0efc0644b4e754bf2183c1c2"
auth_token  = "86f3177a99d46d4cb6237b106be7bd9c"
workspace_sid = "WSa521ebd8b208fe727465ceb9c92bfc52"
worker_sid = args.worker_sid

capability = TaskRouterWorkerCapability(account_sid, auth_token, workspace_sid, worker_sid)
capability.allow_activity_updates()
capability.allow_reservation_updates()


# For example, to generate a token good for 1000 days:
token = capability.generate_token(60 * 60 * 24 * 1000);

print token
