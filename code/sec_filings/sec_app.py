from flask import Flask, request
import requests, json
from sec import Sec
from flask_classful import FlaskView,route

app = Flask(__name__)

r = requests.get('https://www.sec.gov/Archives/edgar/data/1326801/000095010320010143/index.json')
myCo = ''


class SecView(FlaskView):
	def index(self):
		return 'Hello World!'
	
	@route('/insider/<company>')
	def stupid(self,company):
		co_in_question = Sec(company,'insiders')
		return co_in_question.get_filings()
'''@app.route('/insider?co=<co>')
def entry():
	company = requests.arg('co')
	content = json.loads(r.text)
	return content'''

SecView.register(app)
if __name__ == '__main__':
	app.run()
