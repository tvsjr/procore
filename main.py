import base64
import hashlib
import os
import time
from datetime import (
    datetime
)

from flask import (
    Flask,
    render_template,
    request,
    jsonify
)
from waitress import (
    serve
)

# Define global variables for request tracking
requestsInProgress = 0
processNewRequests = 1

# Define global variables for statistics
requestsCompleted = 0
averageTime = 0.0

# Instantiate our web app
webApp = Flask(__name__, template_folder="templates")

# Response for GET /
# Replies with HTML-formatted page with usage info
@webApp.route('/')
def default():
    # Return a default instructions page
    return render_template('default.html')

# Response for POST /hash
# Replies with a base64-encoded SHA512 hash of the value passed in via the password variable
@webApp.route('/hash', methods=['POST'])
def hash():
    # Define our globals
    global requestsInProgress
    global processNewRequests
    global requestsCompleted
    global averageTime

    # New requests will not be processed if a shutdown has been requested
    if processNewRequests == 1:
        # Log start time
        start_time = datetime.now()
        # Track the new request in progress
        requestsInProgress += 1
        # Wait 5 seconds before responding, per application requirements
        time.sleep(5)
        # Ensure we have a "password" input
        if "password" not in request.form:
            requestsInProgress -= 1
            return "A password was not specified!"
        else:
            # We have a valid request. Calculate the hash
            return_value = base64.b64encode(hashlib.sha512(request.form['password'].encode('utf-8')).digest())

            # Calculate the elapsed time, plus 5000ms to account for the sleep period
            elapsed_time = ((datetime.now() - start_time).microseconds / 1000) + 5000

            # Update our statistics
            averageTime = ((averageTime * requestsCompleted) + elapsed_time) / (requestsCompleted + 1)
            requestsCompleted += 1

            # Request is completed, reduce the global in-progress variable by 1 and return our value
            requestsInProgress -= 1
            return return_value
    else:
        # Warn the user that the server is shutting down
        return "Request not processed - server is shutting down"

# Response for GET /shutdown or POST /shutdown
@webApp.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    # Define our globals
    global processNewRequests
    global requestsInProgress

    # Prevent new requests from being processed
    processNewRequests = 0

    # Wait until all requests are complete, then exit with status code 0
    while requestsInProgress > 0:
        time.sleep(1)
    os._exit(0)

# Response for GET /stats or POST /stats
@webApp.route('/stats', methods=['GET', 'POST'])
def stats():
    # Define our globals
    global requestsCompleted
    global averageTime

    # Return a JSON object containing total requests completed and average processing time (rounded to 1ms)
    return jsonify(total=str(requestsCompleted),
                   average=str(round(averageTime)))


# Run the application
serve(webApp, host='0.0.0.0', port=8080)
