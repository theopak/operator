from flask import render_template, request, jsonify, Response
import json
import sendgrid
from bson import json_util
from bson.objectid import ObjectId
import op
import urllib2

from settings import *


@app.route('/')
def home_page():
    '''
    Home page, which is the entire frontend app lol.
    '''
    return render_template('index.html')


@app.route('/companies/search/<query>')
def company_search(query):
    results = list(mongo.db.companies.find({
        'name': {
            '$regex': '^'+query,
            '$options': '-i'
        }
    }))
    return json.dumps(results, default=json_util.default, ensure_ascii=False)


@app.route('/companies/info/<query>')
def company_info(query):
    company = mongo.db.companies.find_one({'name': query})
    return json.dumps(company, default=json_util.default, ensure_ascii=False)


@app.route('/outbound/', methods=['GET'])
def list_outbound():
    '''
    Return a list of all outbound calls logged in the db.
    '''
    refs = list(mongo.db.initiatedCalls.find())
    return json.dumps(refs, default=json_util.default)


@app.route('/outbound/new', methods=['POST', 'PUT'])
def handle_outbound():
    '''
    Place an outbound call.
    '''

    # Detect and handle errors
    if request.form.keys() < 1:
        error = "PUT/POST JSON object (application/json preferred) (application/x-www-form-urlencoded)."
        return render_template('error.html', error=error)

    # Load data as JSON
    document = request.get_json(force=True)
    name = document['outbound']
    phone = document['phone']
    email = document['email']
    sequence = document['sequence']

    sequence = ['w' + x for x in sequence]
    sequence = ''.join(sequence)
    sequence = 'wwww' + sequence

    business = mongo.db.companies.find_one({'name': name})

    # Add each dimension to the collection as a unique document
    ref = mongo.db.initiatedCalls.insert({
        "user_phone": phone,
        "user_email": email,
    })

    print "REF", ref
    op.place_call(business['phone'], ref, sequence)

    # Return success
    data = {'result': 'success'}
    return json.dumps(data, default=json_util.default)

@app.route('/inbound/connected/<uid>/<sequence>', methods=['POST', 'PUT'])
def handle_inbound(uid, sequence):
    sid = request.form['CallSid']
    return Response(op.press_buttons(sid, uid, sequence), mimetype="text/xml")

@app.route('/inbound/waiting/<uid>', methods=['POST', 'PUT'])
def handle_wait(uid):
    return Response(op.loop_human_check(uid), mimetype="text/xml")

@app.route('/inbound/complete/<uid>')
def handle_complete(uid):
    print uid
    user_phone = mongo.db.initiatedCalls.find_one({'_id': ObjectId(uid)})
    print user_phone
    user_phone = user_phone['user_phone']
    return Response(op.call_user(user_phone, uid), mimetype="text/xml")

@app.route('/inbound/record-complete/<uid>', methods=['POST', 'PUT'])
def handle_record_complete(uid):
    user_email = mongo.db.initiatedCalls.find_one({'_id': ObjectId(uid)})['user_email']
    recording = urllib2.urlopen(request.form['RecordingUrl'])
    message = sendgrid.Mail(to=user_email, subject='Your Operator Recording', text=request.form['TranscriptionText'], from_email='no-reply@happyoperator.com')
    message.add_attachment_stream("recording.mp3", recording.read())
    status, msg = sg.send(message)

    return ""


if __name__ == "__main__":
    app.debug = True  # Do not enable Debug mode on the production server!
    app.run(port=8001)
