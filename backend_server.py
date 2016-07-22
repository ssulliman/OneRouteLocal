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


@app.route("/worker_dashboard")
def show_worker_dashboard():
    return render_template('worker_dashboard.html')


@app.route("/get_worker_details", methods=['GET', 'POST'])
def get_worker_sid():
    username = request.args.get('user')
    password = request.args.get('pass')

    cursor_count = db.workers.find({'username':username,'password':password}).count()
    print "Worker query returned " + str(cursor_count) + " results.\n\n\n\n\n"

    responseDict = {}

    if cursor_count > 0:
        cursor = db.workers.find({'username':username,'password':password})
        for doc in cursor:
            json_doc = json.dumps(doc, default=json_util.default)
            json_dict = responseDict = json.loads(json_doc)
    else:
        responseDict["worker_sid"] = ""
        responseDict["worker_token"] = ""

    return jsonify(responseDict);

@app.route("/get_all_workers", methods=['GET', 'POST'])
def get_all_workers():
    for worker in task_router.workers(workspace_sid).list():
        print(worker.friendly_name + "\n")
    resp = Response("{}", status=200, mimetype='application/json')
    return resp

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
