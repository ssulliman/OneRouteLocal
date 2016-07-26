#!/usr/local/bin/python2.7

# Use to get port # from Heroku environment
from os import environ

# JSON import
import json
from bson import json_util

# Flask import
from flask import Flask, flash, Response, jsonify, request, render_template
app = Flask(__name__)
app.secret_key = 'bc730ade0c837ba6c39e' # Random secret key

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
workflow_sid = "WW23312adca9ce4cf87cc3488c1b6dde5d"

# Get our TaskRouter object
task_router = TwilioTaskRouterClient(account_sid, auth_token)

# Define Flask routes
@app.route("/")
def root():
    return render_template('worker_login.html')


@app.route("/worker_dashboard")
def show_worker_dashboard():
    friendly_name = request.args.get('worker_name')
    if (friendly_name):
        return render_template('worker_dashboard.html')
    else:
        print "NOT A GOOD WORKER DASHBOARD REQUEST\n\n\n\n\n\n"
        flash('Permission denied: cannot access worker dashboard without logging in')
        return render_template('worker_login.html')


@app.route("/flash_invalid_login")
def flash_worker_login():
        flash('Permission denied: invalid username and password combination')
        return render_template('worker_login.html')


@app.route("/get_worker_details", methods=['GET', 'POST'])
def get_worker_details():
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


@app.route("/assignment_callback", methods=['GET','POST'])
def assignment_callback():
    """Respond to assignment callbacks with empty 200 response"""
    print "Accepted task...\n\n"
    return jsonify({"instruction":"accept"})


@app.route("/create_task", methods=['GET', 'POST'])
def create_task():
    """Create a task with a given list of attributes"""

    task = task_router.tasks(workspace_sid).create(
        workflow_sid=workflow_sid,
        attributes=request.data
        )

    responseDict = {}
    responseDict["task_sid"] = task.sid
    # TODO - add/update task/event to mongodb


    return jsonify(responseDict)


if __name__ == "__main__":
    port = int(environ.get('PORT', 5000)) # Get port number from Heroku environment (assigned automatically)
    app.run(debug=True, host='0.0.0.0', port=port)
