from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from flask_oauthlib.client import OAuth
import requests, json

app = Flask(__name__)
app.debug = True
app.secret_key = '01db2bde0282cb3bc4d3eb7503af1fdf1b3d9d75'
oauth = OAuth(app)


oauth = OAuth()

stocktwits = oauth.remote_app(
	'stocktwits',
	consumer_key= '3a118e125fd6c0f3',
	consumer_secret= '01db2bde0282cb3bc4d3eb7503af1fdf1b3d9d75',
	request_token_params = {'scope':'watchlists'},
	base_url='https://api.stocktwits.com/api/2',
	request_token_url=None,
	access_token_method = 'POST',
	access_token_url='https://api.stocktwits.com/api/2/oauth/token',
	authorize_url = 'https://api.stocktwits.com/api/2/oauth/authorize',
	content_type='application/json'
)

@app.route('/')
def index():
	if 'st_token' in session:
		me = stocktwits.get('user')
		return jsonify(me.data)
	return redirect(url_for('login'))

@app.route('/login')
def login():
	return stocktwits.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
	session.pop('stocktwits_token', None)
	return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
	return render_template('index.php')


@app.route('/friends')
def get_friends():
	resp = requests.get('https://api.stocktwits.com/api/2/streams/friends.json?access_token=' + session.get('st_token'))
	return resp.content 

@app.route('/portal')
def landing():
	if 'st_token' in session:
		# me = stocktwits.get('user')
		return render_template('welcome.php')
	return redirect(url_for('login'))

@app.route('/welcome')
def hello():
	tokenN = ""
	'''with open("./" + request.args.get('user') + ".txt") as tf:
		tokenN = tf.readline()
	tf.close()'''
	st_req = {
		 'client_id':'3a118e125fd6c0f3',
		 'client_secret':'01db2bde0282cb3bc4d3eb7503af1fdf1b3d9d75',
		 'grant_type':'authorization_code',
		 'redirect_uri':'https://gorwellconsulting.com:5000/sweet',
		 'code':request.args.get('code')};
	resp = requests.post('https://api.stocktwits.com/api/2/oauth/token',data=st_req)
	# me = stocktwits.get('user')
	data = json.loads(resp.content)
	session['st_token'] = data['access_token']
	userInfo = json.dumps(data)
	fileName = "./" + str(data['user_id']) + ".json"
	with open(fileName,"w") as jf:
		jf.write(userInfo)
	jf.close()
	return redirect('/portal') # render_template('welcome.php')
	# return jsonify(me.data)

	# return request.args.get('code')
	# return "Token? [{}]".format(tokenN)

'''@app.route('/login/authorized')
def authorized():
	resp = stocktwits.authorized_response()
	if resp is None or resp.get('access_token') is None:
		return 'Access denied: reason=%s error=%s resp=%s' % (
			request.args['error'],
			request.args['error_description'],
			resp
		)
	session['stocktwits_token'] = (resp['access_token'], '')
	me = stocktwits.get('user')
	return jsonify(me.data)
'''
@stocktwits.tokengetter
def get_stocktwits_oauth_token(token=None):
	if token == 'user':
		return session.get('st_token')
	elif token == 'app':
		return 'awesome'
	else: return token
	# raise RuntimeError('invalid butt')
	# return session.get('stocktwits_token')

if __name__ == '__main__':
	app.run()

	
oauth.init_app(app)
