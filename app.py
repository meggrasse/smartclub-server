from flask import Flask
import json
import pickle

app = Flask(__name__)

app_state = {'upvotes': 0, 'downvotes': 0}
pickle.dump( app_state, open( "app_state.p", "wb" ) )

@app.route('/')
def hello_world():
    return 'Hello World!'

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

@app.route('/sendtunes', methods=['GET', 'POST'])
def sendtunes():
    return request.form['music']

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
