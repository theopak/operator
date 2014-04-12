from flask import Flask, render_template, request, jsonify, Response
#import logging
import json
from flask.ext.pymongo import PyMongo


# Connect to remote MongoDB instance
app = Flask(__name__, static_folder='static')
# app.config['MONGO_HOST'] = '0.mongolab.com'
# app.config['MONGO_PORT'] = 0
# app.config['MONGO_DBNAME'] = 'dbname'
# app.config['MONGO_USERNAME'] = 'username'
# app.config['MONGO_PASSWORD'] = 'password'
# mongo = PyMongo(app, config_prefix='MONGO')


@app.route('/')
def home_page():
    '''
    Home page
    '''
    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True  # Do not enable Debug mode on the production server!
    app.run()
