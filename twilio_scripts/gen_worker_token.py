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
account_sid = "AC18175a2369f4b32507c12549a8a6b44f"
auth_token  = "edda94dfd34d1bf0c8e2d6cf789dd04f"
workspace_sid = "WS43206b368788de2027c551fcf7264500"
worker_sid = args.worker_sid

capability = TaskRouterWorkerCapability(account_sid, auth_token, workspace_sid, worker_sid)
capability.allow_activity_updates()
capability.allow_reservation_updates()

# For example, to generate a token good for 1000 days:
token = capability.generate_token(60 * 60 * 24 * 1000);

print token