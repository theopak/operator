from flask import Flask, render_template, request, jsonify, Response
#import logging
import json
from flask.ext.pymongo import PyMongo
from bson import json_util


# Connect to remote MongoDB instance
app = Flask(__name__, static_folder='static')
mongo = PyMongo(app, config_prefix='MONGO')


@app.route('/')
def home_page():
    '''
    Home page, which is the entire frontend app lol.
    '''
    return render_template('index.html')


@app.route('/outbound/new', methods=['POST', 'PUT'])
def handle_outbound():
    '''
    Place an outbound call.
    '''

    # Useful for debugging
    print request.form
    document = request.form[0]

    # Detect and handle errors
    if request.form.keys() < 1:
        error = "PUT/POST JSON object (application/x-www-form-urlencoded)."
        return render_template('error.html', error=error)

    # Add each dimension to the collection as a unique document
    refs = mongo.db.initiatedCalls.insert(document)

    # Return success
    data = {'result': 'success'}
    return json.dumps(data, default=json_util.default)


if __name__ == "__main__":
    app.debug = True  # Do not enable Debug mode on the production server!
    app.run()
