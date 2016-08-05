#!/usr/local/bin/python2.7

# Use to get port # from Heroku environment
from os import environ

# JSON import
import json
from bson import json_util

#Import Logger
import logging
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('event.log')
handler.setLevel(logging.INFO)

# create a logging format

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger

logger.addHandler(handler)


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

#Twilio Voice Client
voice_client = TwilioRestClient(account_sid, auth_token)

# Define Flask routes
# =========== HTML Routes ===========
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

# =========== Twilio Routes ===========
@app.route("/event_callback", methods=['GET','POST'])
def event_callback():
    """Respond to events"""
    form_dict = request.form

    #TODO-Create Accept Call function that accepts the call to the phone number provided by the worker
    #TODO-Make Outgoing call to twilio number that mimics our flow

    #Switch on EventType for Task Events
    if(form_dict["EventType"] == "task.created"):
        task_dict = {"task_sid":form_dict["TaskSid"], "task_attributes":form_dict["TaskAttributes"], "task_age":form_dict["TaskAge"], "task_assigment_status":form_dict["TaskAssignmentStatus"], "task_reason":"None" }
        db.tasks.insert(task_dict)
        log_message = "Task Sid: %s, Task Attributes: %s, Task Age: %s, Task Status: %s" %(form_dict["TaskSid"],form_dict["TaskAttributes"],form_dict["TaskAge"],form_dict["TaskAssignmentStatus"])
        print "" %(form_dict["TaskSid"])
        print "Task Attributes: %s" % (form_dict["TaskAttributes"])
        print "Task Age: %s" %(form_dict["TaskAge"])
        print "Task Status: %s" %(form_dict["TaskAssignmentStatus"])
        print "Task Creation"
        logger.info()

    elif(form_dict["EventType"] == "task.cancelled"):
        #TODO-Find the task and update it to cancelled and give the reason why it was cancelled
        task_cursor = db.tasks.update_on({"task_sid": form_dict["TaskSid"]}, {"task_assignment_status": form_dict["TaskAssignmentStatus"], "task_reason": form_dict["TaskCancelledReason"]})
        print "Task Sid: %s" %(form_dict["TaskSid"])
        print "Task Attributes: %s" % (form_dict["TaskAttributes"])
        print "Task Age: %s" %(form_dict["TaskAge"])
        print "Task Status: %s" %(form_dict["TaskAssignmentStatus"])
        print "Task Cancelled"

    elif(form_dict["EventType"] == "task.completed"):
        #TODO-Find the task in Mongo and update to Completed
        task_cursor = db.tasks.update_on({"task_sid": form_dict["TaskSid"]}, {"task_assignment_status": form_dict["TaskAssignmentStatus"], "task_reason": form_dict["TaskCompletedReason"]})
        print "Task Sid: %s" %(form_dict["TaskSid"])
        print "Task Attributes: %s" % (form_dict["TaskAttributes"])
        print "Task Age: %s" %(form_dict["TaskAge"])
        print "Task Status: %s" %(form_dict["TaskAssignmentStatus"])
        print "Task Completed"

    elif(form_dict["EventType"] == "task.updated"):
        #task_cursor = db.tasks.update_on({"task_sid": form_dict["TaskSid"]}, {"task_assignment_status": form_dict["TaskAssignmentStatus"], "task_reason": "None")
        return
    elif(form_dict["EventType"] == "task.deleted"):
        #TODO-Find task and update the deletion
        db.tasks.update_on({"task_sid": form_dict["TaskSid"]}, {"task_assignment_status": form_dict["TaskAssignmentStatus"], "task_reason": form_dict["TaskDeletedReason"]})
        print "Task Sid: %s" %(form_dict["TaskSid"])
        print "Task Attributes: %s" % (form_dict["TaskAttributes"])
        print "Task Age: %s" %(form_dict["TaskAge"])
        print "Task Status: %s" %(form_dict["TaskAssignmentStatus"])
        print "Task Deleted"

    #Switch on EventType for Worker Event
    elif(form_dict["EventType"] == "worker.activity.update"):
        print "Worker activity Update"
    elif(form_dict["EventType"] == "worker.attributes.update"):
        print "Worker Attributes Update"

    #Switch on EventType for Reservation Events
    elif(form_dict["EventType"] == "reservation.created"):
        print "Reservation is Created"

    elif(form_dict["EventType"] == "reservation.accepted"):
        print "Making a call to a phone number"
        print "\nReservation is accepted"
        task_sid = form_dict["TaskSid"]
        task = task_router.tasks(workspace_sid).get(task_sid)
        print task.attributes
        call = voice_client.calls.create(url="http://demo.twilio.com/docs/voice.xml", to=task.attributes["phone_number"], from_="+14082146768")
        print(call.sid)

    elif(form_dict["EventType"] == "reservation.rejected"):
        print "Reservation is Rejected"
    elif(form_dict["EventType"] == "reservation.timeout"):
        print "Reservation is timed out"
    elif(form_dict["EventType"] == "reservation.cancelled"):
        print "Reservation is Cancelled"
    elif(form_dict["EventType"] == "reservation.rescinded"):
        print "Reservation is Rescinded"

    #Switch on EventType for TaskQueue Events
    elif(form_dict["EventType"] == "task-queue.entered"):
        print "Task entered TaskQueue"
        taskqueue_sid = form_dict["TaskQueueSid"]
        #statistics = task_router.task_queues(workspace_sid).get(taskqueue_sid).statistics.get()
        print form_dict

    elif(form_dict["EventType"] == "task-queue.timeout"):
        print "Task timed out in this TaskQueue"
        taskqueue_sid = form_dict["TaskQueueSid"]
        #statistics = task_router.task_queues(workspace_sid).get(taskqueue_sid).statistics.get()
        print form_dict

    elif(form_dict["EventType"] == "task-queue.moved"):
        print "Task moved into a different TaskQueue"
        taskqueue_sid = form_dict["TaskQueueSid"]
        #statistics = task_router.task_queues(workspace_sid).get(taskqueue_sid).statistics.get()
        print form_dict

    #Switch on EventType for Workflow Events
    elif(form_dict["EventType"] == "workflow.timeout"):
        print "Task has timed out in this workflow"
    elif(form_dict["EventType"] == "workflow.entered"):
        print "Task has entered into this workflow"


    return Response("{}", status=200, mimetype='application/json')


@app.route("/assignment_callback", methods=['GET','POST'])
def assignment_callback():
    """Respond to assignment callbacks with empty 200 response"""
    print "Accepted task...\n\n"
    print request.form
    return jsonify({"instruction":"accept"})


@app.route("/create_task", methods=['GET', 'POST'])
def create_task():
    """Create a task with a given list of attributes"""

    task = task_router.tasks(workspace_sid).create(
        workflow_sid=workflow_sid,
        attributes=request.data
        )

    return jsonify({"task_sid":task.sid})


if __name__ == "__main__":
    port = int(environ.get('PORT', 5000)) # Get port number from Heroku environment (assigned automatically)
    app.run(debug=True, host='0.0.0.0', port=port)
