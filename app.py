from flask import Flask, request
import json
import pickle

app = Flask(__name__)

app_state = {'upvotes': 0, 'downvotes': 0, 'music':[]}
pickle.dump( app_state, open( "app_state.p", "wb" ) )

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/getvotecount')
def getvotes():
    # app_state = pickle.load( open( "app_state.p", "rb" ) )
    output = json.dumps(app_state)
    return output

@app.route('/upvote')
def upvote():
    # app_state = pickle.load( open( "app_state.p", "rb" ) )
    app_state['upvotes'] += 1
    # pickle.dump( app_state, open( "app_state.p", "wb" ) )
    output = json.dumps(app_state)
    return output

@app.route('/downvote')
def downvote():
    # app_state = pickle.load( open( "app_state.p", "rb" ) )
    app_state['downvotes'] += 1
    # pickle.dump( app_state, open( "app_state.p", "wb" ) )
    output = json.dumps(app_state)
    return output

@app.route('/clearvotes')
def clearvotes():
    # app_state = pickle.load( open( "app_state.p", "rb" ) )
    app_state['downvotes'] = 0
    app_state['upvotes'] = 0
    # pickle.dump( app_state, open( "app_state.p", "wb" ) )
    output = json.dumps(app_state)
    return output

@app.route('/sendtunes', methods=['POST'])
def sendtunes():
    dt = request.form['music']
    app_state['music'].extend(dt)
    return json.dumps(app_state['music'])

@app.route('/wasthereascream')
def wasthereascream():
    # app_state = pickle.load( open( "app_state.p", "rb" ) )
    if 255 in app_state['music']:
        return 'Yes'
    else:
        return 'No'

@app.route('/gettunes')
def gettunes():
    return json.dumps(app_state['music'])

@app.route('/resetscreamtracker')
def resetscream():
    # app_state = pickle.load( open( "app_state.p", "rb" ) )
    app_state['music'] = []
    # pickle.dump( app_state, open( "app_state.p", "wb" ) )
    return 'OK'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
