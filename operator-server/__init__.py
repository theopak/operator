from flask import render_template, request, jsonify, Response
import json
from bson import json_util

from settings import *

@app.route('/')
def home_page():
    '''
    Home page
    '''
    return render_template('index.html')

@app.route('/companies/<query>.json')
def company_search(query):
    results = list(mongo.db.companies.find({'name': {'$regex': query, '$options': '-i'}}))
    return json.dumps(results, default=json_util.default)

if __name__ == "__main__":
    app.debug = True  # Do not enable Debug mode on the production server!
    app.run()
