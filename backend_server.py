#!/usr/local/bin/python2.7

# Use to get port # from Heroku environment
from os import environ

# JSON import
import json
from bson import json_util

# Flask import
from flask import Flask, Response, jsonify, request, render_template
app = Flask(__name__)

# Mongo import and connection to OneRoute database
from pymongo import MongoClient
# The following is the MongoDB URI that we obtain from mLab
# mLab is our Heroku MongoDB provider
mongo_user = "one_route_dev"
mongo_pass = "oneroutedev"
mongo_client = MongoClient('mongodb://' + mongo_user + ':' + mongo_pass + '@ds027145.mlab.com:27145/one_route')
db = mongo_client.one_route

# Twilio import
from twilio.rest import TwilioTaskRouterClient, TwilioRestClient
from twilio.rest.exceptions import TwilioRestException

# Twilio account details
account_sid = "ACc9111e5c0efc0644b4e754bf2183c1c2"
auth_token  = "86f3177a99d46d4cb6237b106be7bd9c"
workspace_sid = "WSa521ebd8b208fe727465ceb9c92bfc52"
workflow_sid = "WWff7e028b12767a53586b351a3b4b6afe"

# Get our TaskRouter object
task_router = TwilioTaskRouterClient(account_sid, auth_token)

# Define Flask routes

@app.route("/")
def root():
    return render_template('worker_login.html')

@app.route("/add_worker")
def add_dummy_worker():
    db.workers.insert({"username":"test@test.com", "password":"test", "worker_sid":"WK46c16e3fb0551241f479f0031d473162", "worker_token":"eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJleHAiOiAxNTU1NTU2MTMwLCAiaXNzIjogIkFDMTgxNzVhMjM2OWY0YjMyNTA3YzEyNTQ5YThhNmI0NGYiLCAid29ya3NwYWNlX3NpZCI6ICJXUzQzMjA2YjM2ODc4OGRlMjAyN2M1NTFmY2Y3MjY0NTAwIiwgImZyaWVuZGx5X25hbWUiOiAiV0s0NmMxNmUzZmIwNTUxMjQxZjQ3OWYwMDMxZDQ3MzE2MiIsICJhY2NvdW50X3NpZCI6ICJBQzE4MTc1YTIzNjlmNGIzMjUwN2MxMjU0OWE4YTZiNDRmIiwgInZlcnNpb24iOiAidjEiLCAicG9saWNpZXMiOiBbeyJ1cmwiOiAiaHR0cHM6Ly9ldmVudC1icmlkZ2UudHdpbGlvLmNvbS92MS93c2NoYW5uZWxzL0FDMTgxNzVhMjM2OWY0YjMyNTA3YzEyNTQ5YThhNmI0NGYvV0s0NmMxNmUzZmIwNTUxMjQxZjQ3OWYwMDMxZDQ3MzE2MiIsICJwb3N0X2ZpbHRlciI6IHt9LCAibWV0aG9kIjogIkdFVCIsICJhbGxvdyI6IHRydWUsICJxdWVyeV9maWx0ZXIiOiB7fX0sIHsidXJsIjogImh0dHBzOi8vZXZlbnQtYnJpZGdlLnR3aWxpby5jb20vdjEvd3NjaGFubmVscy9BQzE4MTc1YTIzNjlmNGIzMjUwN2MxMjU0OWE4YTZiNDRmL1dLNDZjMTZlM2ZiMDU1MTI0MWY0NzlmMDAzMWQ0NzMxNjIiLCAicG9zdF9maWx0ZXIiOiB7fSwgIm1ldGhvZCI6ICJQT1NUIiwgImFsbG93IjogdHJ1ZSwgInF1ZXJ5X2ZpbHRlciI6IHt9fSwgeyJ1cmwiOiAiaHR0cHM6Ly90YXNrcm91dGVyLnR3aWxpby5jb20vdjEvV29ya3NwYWNlcy9XUzQzMjA2YjM2ODc4OGRlMjAyN2M1NTFmY2Y3MjY0NTAwL1dvcmtlcnMvV0s0NmMxNmUzZmIwNTUxMjQxZjQ3OWYwMDMxZDQ3MzE2MiIsICJwb3N0X2ZpbHRlciI6IHt9LCAibWV0aG9kIjogIkdFVCIsICJhbGxvdyI6IHRydWUsICJxdWVyeV9maWx0ZXIiOiB7fX0sIHsidXJsIjogImh0dHBzOi8vdGFza3JvdXRlci50d2lsaW8uY29tL3YxL1dvcmtzcGFjZXMvV1M0MzIwNmIzNjg3ODhkZTIwMjdjNTUxZmNmNzI2NDUwMC9BY3Rpdml0aWVzIiwgInBvc3RfZmlsdGVyIjoge30sICJtZXRob2QiOiAiR0VUIiwgImFsbG93IjogdHJ1ZSwgInF1ZXJ5X2ZpbHRlciI6IHt9fSwgeyJ1cmwiOiAiaHR0cHM6Ly90YXNrcm91dGVyLnR3aWxpby5jb20vdjEvV29ya3NwYWNlcy9XUzQzMjA2YjM2ODc4OGRlMjAyN2M1NTFmY2Y3MjY0NTAwL1Rhc2tzLyoqIiwgInBvc3RfZmlsdGVyIjoge30sICJtZXRob2QiOiAiR0VUIiwgImFsbG93IjogdHJ1ZSwgInF1ZXJ5X2ZpbHRlciI6IHt9fSwgeyJ1cmwiOiAiaHR0cHM6Ly90YXNrcm91dGVyLnR3aWxpby5jb20vdjEvV29ya3NwYWNlcy9XUzQzMjA2YjM2ODc4OGRlMjAyN2M1NTFmY2Y3MjY0NTAwL1dvcmtlcnMvV0s0NmMxNmUzZmIwNTUxMjQxZjQ3OWYwMDMxZDQ3MzE2Mi9SZXNlcnZhdGlvbnMvKioiLCAicG9zdF9maWx0ZXIiOiB7fSwgIm1ldGhvZCI6ICJHRVQiLCAiYWxsb3ciOiB0cnVlLCAicXVlcnlfZmlsdGVyIjoge319LCB7InVybCI6ICJodHRwczovL3Rhc2tyb3V0ZXIudHdpbGlvLmNvbS92MS9Xb3Jrc3BhY2VzL1dTNDMyMDZiMzY4Nzg4ZGUyMDI3YzU1MWZjZjcyNjQ1MDAvV29ya2Vycy9XSzQ2YzE2ZTNmYjA1NTEyNDFmNDc5ZjAwMzFkNDczMTYyIiwgInBvc3RfZmlsdGVyIjogeyJBY3Rpdml0eVNpZCI6IHsicmVxdWlyZWQiOiB0cnVlfX0sICJtZXRob2QiOiAiUE9TVCIsICJhbGxvdyI6IHRydWUsICJxdWVyeV9maWx0ZXIiOiB7fX0sIHsidXJsIjogImh0dHBzOi8vdGFza3JvdXRlci50d2lsaW8uY29tL3YxL1dvcmtzcGFjZXMvV1M0MzIwNmIzNjg3ODhkZTIwMjdjNTUxZmNmNzI2NDUwMC9UYXNrcy8qKiIsICJwb3N0X2ZpbHRlciI6IHt9LCAibWV0aG9kIjogIlBPU1QiLCAiYWxsb3ciOiB0cnVlLCAicXVlcnlfZmlsdGVyIjoge319LCB7InVybCI6ICJodHRwczovL3Rhc2tyb3V0ZXIudHdpbGlvLmNvbS92MS9Xb3Jrc3BhY2VzL1dTNDMyMDZiMzY4Nzg4ZGUyMDI3YzU1MWZjZjcyNjQ1MDAvV29ya2Vycy9XSzQ2YzE2ZTNmYjA1NTEyNDFmNDc5ZjAwMzFkNDczMTYyL1Jlc2VydmF0aW9ucy8qKiIsICJwb3N0X2ZpbHRlciI6IHt9LCAibWV0aG9kIjogIlBPU1QiLCAiYWxsb3ciOiB0cnVlLCAicXVlcnlfZmlsdGVyIjoge319XSwgImNoYW5uZWwiOiAiV0s0NmMxNmUzZmIwNTUxMjQxZjQ3OWYwMDMxZDQ3MzE2MiIsICJ3b3JrZXJfc2lkIjogIldLNDZjMTZlM2ZiMDU1MTI0MWY0NzlmMDAzMWQ0NzMxNjIifQ.Lgu1yK6l3aqcbpfqPGdf7A604FS49oU3OZWFjJNpZ3g"})
    resp = Response("{}", status=200, mimetype='application/json')
    return resp

@app.route("/worker_dashboard")
def show_worker_dashboard():
    return render_template('worker_dashboard.html')


@app.route("/get_worker_sid", methods=['GET', 'POST'])
def get_worker_sid():
    username = request.args.get('user')
    password = request.args.get('pass')
    worker = {}
    worker[username] = username
    worker[password] = password

    responseDict = {}

    cursor_count = db.workers.find(worker).count()
    print "Worker query returned " + str(cursor_count) + " results.\n\n\n\n\n"

    if cursor_count > 0:
        cursor = db.workers.find(worker)
        for doc in cursor:
            json_doc = json.dumps(doc, default=json_util.default)
            json_dict = json.loads(json_doc)
            responseDict["worker_sid"] = json_dict["worker_sid"]
            responseDict["worker_token"] = json_dict["worker_token"]
    else:
        print "Got 0 results from mongodb - check connection or db content +++++++++++++++++++\n\n\n\n"
        responseDict["worker_sid"] = ""
        responseDict["worker_token"] = ""

    print responseDict
    return jsonify(responseDict);

@app.route("/twilio_callback", methods=['GET', 'POST'])
def twilio_callback():
    """Respond to ANY event within the Twilio workspace"""
    resp = Response("{}", status=200, mimetype='application/json')
    return resp


@app.route("/assignment_callback", methods=['GET','POST'])
def assignment_callback():
    """Respond to assignment callbacks with empty 200 response"""
    
    resp = Response("{}", status=200, mimetype='application/json')
    return resp


@app.route("/create_task", methods=['GET', 'POST'])
def create_task():
    """Create a task"""
    task = task_router.tasks(workspace_sid).create(
        workflow_sid=workflow_sid,
        attributes='{"selected_language":"ru"}'
        )
    print task.sid
    resp = Response(task.attributes, status=200, mimetype='application/json')
    return resp


@app.route("/accept_reservation", methods=['GET', 'POST'])
def accept_reservation(task_sid, reservation_sid):
    """Accept reservation"""
    task_sid = request.args.get('task_sid')
    reservation_sid = request.args.get('reservation_sid')

    reservation = client.reservations(workspace_sid, task_sid).update(reservation_sid, reservation_station='accepted')
    print reservation.reservation_status
    print reservation.worker_name

    resp = Response('%s, %s'%(reservation.reservation_status, reservation.worker_name), status=200, mimetype='application/json')
    return resp


if __name__ == "__main__":
    port = int(environ.get('PORT', 5000)) # Get port number from Heroku environment (assigned automatically)
    app.run(debug=True, host='0.0.0.0', port=port)
