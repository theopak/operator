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
    name = document['input-name']
    phone = document['input-number']
    sequence = document['sequence']

    business = mongo.db.companies.find_one({'name': name})
    op.place_call(business['phone'], sequence)

    # Add each dimension to the collection as a unique document
    # refs = mongo.db.initiatedCalls.insert(document)

    # Return success
    data = {'result': 'success', 'results': refs}
    return json.dumps(data, default=json_util.default)


@app.route('/inbound/connected/<sequence>')
def handle_inbound(sequence):
    return op.press_buttons(None, sequence)


if __name__ == "__main__":
    app.debug = True  # Do not enable Debug mode on the production server!
    app.run()
