from flask import Flask, request
import json
import pickle
import threading
import time
import logging
import random
import os

app = Flask(__name__)

app_state = {'upvotes': 0, 'downvotes': 0, 'music':[], '1':[], '2':[]}
pickle.dump(app_state, open('app_state.p', 'wb'))

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/getappstate')
def getappstate():
    app_state = pickle.load(open('app_state.p', 'rb'))
    return json.dumps(app_state)

@app.route('/getvotecount')
def getvotes():
    app_state = pickle.load(open('app_state.p', 'rb'))
    retdict = {}
    retdict['upvotes'] = app_state['upvotes']
    retdict['downvotes'] = app_state['downvotes']
    output = json.dumps(retdict)
    return output

@app.route('/upvote')
def upvote():
    app_state = pickle.load(open('app_state.p', 'rb'))
    app_state['upvotes'] += 1
    pickle.dump(app_state, open('app_state.p', 'wb'))
    output = json.dumps(app_state)
    return output

@app.route('/downvote')
def downvote():
    app_state = pickle.load(open('app_state.p', 'rb'))
    app_state['downvotes'] += 1
    pickle.dump(app_state, open('app_state.p', 'wb'))
    output = json.dumps(app_state)
    return output

@app.route('/clearvotes')
def clearvotes():
    app_state = pickle.load(open('app_state.p', 'rb'))
    app_state['downvotes'] = 0
    app_state['upvotes'] = 0
    pickle.dump(app_state, open('app_state.p', 'wb'))
    output = json.dumps(app_state)
    return output

@app.route('/sendtunes', methods=['POST'])
def sendtunes():
    dt = request.form['music']
    dt = json.loads(dt)
    app_state = pickle.load(open('app_state.p', 'rb'))
    app_state['music'].extend(dt)
    pickle.dump(app_state, open('app_state.p', 'wb'))
    return json.dumps(app_state['music'])

@app.route('/wasthereascream')
def wasthereascream():
    app_state = pickle.load(open('app_state.p', 'rb'))
    if 255 in app_state['music']:
        return 'Yes'
    else:
        return 'No'

@app.route('/gettunes')
def gettunes():
    app_state = pickle.load(open('app_state.p', 'rb'))
    return json.dumps(app_state['music'])

@app.route('/resetscreamtracker')
def resetscream():
    app_state = pickle.load(open('app_state.p', 'rb'))
    app_state['music'] = []
    pickle.dump(app_state, open('app_state.p', 'wb'))
    return 'OK'
    
if __name__ == '__main__':
    # app.run(debug=True, use_reloader=False)
    app.run(host='0.0.0.0', port=1024, debug=False, use_reloader=False)
