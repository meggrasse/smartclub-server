from flask import Flask, request
import json
import pickle
import threading
import time
import logging
import random
import os
from twilio.rest import TwilioRestClient

app = Flask(__name__)
try:
    from config import ACCOUNT_SID, AUTH_TOKEN
    os.environ['ACCOUNT_SID'] = ACCOUNT_SID
    os.environ['AUTH_TOKEN'] = AUTH_TOKEN
    print os.environ['AUTH_TOKEN']
except:
    pass

app_state = {'upvotes': 0, 'downvotes': 0, 'music':[], '1':[], '2':[]}
pickle.dump( app_state, open( "app_state.p", "wb" ) )

client = TwilioRestClient(os.environ['ACCOUNT_SID'], os.environ['AUTH_TOKEN'])

class poll_for_imbalance_in_people_distribution(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.id = random.random()
        self.lastone = None
    def run(self):
        app.logger.debug("HI!")
        while True:
            app_state = pickle.load( open( "app_state.p", "rb" ) )
            if len(app_state['1']) > len(app_state['2']) and self.lastone is not 1:
                self.lastone = 1
                print "ONE", self.id
                message = client.messages.create(body="Hey server, there are lots of people over by the dance floor!", to="+19145845033", from_="+1 630-755-6548")
            elif len(app_state['1']) < len(app_state['2']) and self.lastone is not 2:
                self.lastone = 2
                print "TWO", self.id
                message = client.messages.create(body="Hey server, there are lots of people over by the bar!", to="+19145845033", from_="+1 630-755-6548")
            time.sleep(3)

# initialize polling
t1 = poll_for_imbalance_in_people_distribution()
t1.start()

@app.route('/')
def hello_world():
    app.logger.debug("OWAH~!")
    return 'Hello World!'

@app.route('/getappstate')
def getappstate():
    app_state = pickle.load( open( "app_state.p", "rb" ) )
    return json.dumps(app_state)

@app.route('/getvotecount')
def getvotes():
    app_state = pickle.load( open( "app_state.p", "rb" ) )
    retdict = {}
    retdict['upvotes'] = app_state['upvotes']
    retdict['downvotes'] = app_state['downvotes']
    output = json.dumps(retdict)
    return output

@app.route('/upvote')
def upvote():
    app_state = pickle.load( open( "app_state.p", "rb" ) )
    app_state['upvotes'] += 1
    pickle.dump( app_state, open( "app_state.p", "wb" ) )
    output = json.dumps(app_state)
    return output

@app.route('/downvote')
def downvote():
    app_state = pickle.load( open( "app_state.p", "rb" ) )
    app_state['downvotes'] += 1
    pickle.dump( app_state, open( "app_state.p", "wb" ) )
    output = json.dumps(app_state)
    return output

@app.route('/clearvotes')
def clearvotes():
    app_state = pickle.load( open( "app_state.p", "rb" ) )
    app_state['downvotes'] = 0
    app_state['upvotes'] = 0
    pickle.dump( app_state, open( "app_state.p", "wb" ) )
    output = json.dumps(app_state)
    return output

@app.route('/sendtunes', methods=['POST'])
def sendtunes():
    dt = request.form['music']
    dt = json.loads(dt)
    app_state = pickle.load( open( "app_state.p", "rb" ) )
    app_state['music'].extend(dt)
    pickle.dump( app_state, open( "app_state.p", "wb" ) )
    return json.dumps(app_state['music'])

@app.route('/wasthereascream')
def wasthereascream():
    app_state = pickle.load( open( "app_state.p", "rb" ) )
    if 255 in app_state['music']:
        return 'Yes'
    else:
        return 'No'

@app.route('/gettunes')
def gettunes():
    app_state = pickle.load( open( "app_state.p", "rb" ) )
    return json.dumps(app_state['music'])

@app.route('/resetscreamtracker')
def resetscream():
    app_state = pickle.load( open( "app_state.p", "rb" ) )
    app_state['music'] = []
    pickle.dump( app_state, open( "app_state.p", "wb" ) )
    return 'OK'

@app.route('/1/<uuid>')
def one(uuid):
    app_state = pickle.load( open( "app_state.p", "rb" ) )
    if uuid not in app_state['1']:
        app_state['1'].append(uuid)
        if uuid in app_state['2']:
            app_state['2'].remove(uuid)
    pickle.dump( app_state, open( "app_state.p", "wb" ) )
    return 'OK'

@app.route('/2/<uuid>')
def two(uuid):
    app_state = pickle.load( open( "app_state.p", "rb" ) )
    if uuid not in app_state['2']:
        app_state['2'].append(uuid)
        if uuid in app_state['1']:
            app_state['1'].remove(uuid)
    pickle.dump( app_state, open( "app_state.p", "wb" ) )
    return 'OK'

if __name__ == '__main__':
    # app.run(debug=True, use_reloader=False)
    app.run(host="0.0.0.0", port=80, debug=False, use_reloader=False)
