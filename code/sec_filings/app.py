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
	
# @route('/insider/<company>/<yr>/<qtr>/',defaults={'company':None,'yr':None,'qtr':None})
	@route('/insider/<company>/')
	def insider(self,company):
		co_in_question = Sec(company, 'insiders')
		json_data = co_in_question.get_co_links_json(co_in_question.get_co_seed(),'4')
		return co_in_question.get_filings()

	def get_filing_urls(self,company):
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
