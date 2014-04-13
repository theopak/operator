from flask import render_template, request, jsonify, Response
import json
from bson import json_util
import op

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


@app.route('/outbound/new', methods=['POST', 'PUT'])
def handle_outbound():
    '''
    Place an outbound call.
    '''

    # Useful for debugging
    # print request.form
    # document = request.form[0]

    # Detect and handle errors
    # if request.form.keys() < 1:
    #     error = "PUT/POST JSON object (application/x-www-form-urlencoded)."
    #     return render_template('error.html', error=error)

    # name = request.form['input-name']
    # phone = request.form['input-number']
    sequence = request.form['sequence']

    sequence = ['w' + x for x in sequence]
    sequence = ''.join(sequence)
    sequence = 'wwwwww' + sequence
    print sequence

    op.place_call("+16034756914", sequence)

    # Add each dimension to the collection as a unique document
    # refs = mongo.db.initiatedCalls.insert(document)

    # Return success
    data = {'result': 'success'}
    return json.dumps(data, default=json_util.default)

@app.route('/inbound/connected/<sequence>', methods=['POST', 'PUT'])
def handle_inbound(sequence):
    sid = request.form['CallSid']
    return Response(op.press_buttons(sid, sequence), mimetype="text/xml")


if __name__ == "__main__":
    app.debug = True  # Do not enable Debug mode on the production server!
    app.run(port=8001)
