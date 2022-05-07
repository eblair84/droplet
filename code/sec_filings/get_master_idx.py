import requests,os.path, time
import xml.etree.ElementTree as ET
from os import path
import re
import json
from bs4 import BeautifulSoup

class Sec:
	sec_index_url = r"https://www.sec.gov/Archives/edgar/full-index/"
	filing_base_url = r"https://www.sec.gov/Archives/edgar/data"
	sec_url = r"https://www.sec.gov"
	num_new_files = 0
	ticker_query = "" 
	co_seed = "" 
	form_in_question = "10-q"
	
	def __init__(self):
		self.co_seed = "fb"
		form_in_question = "10-q"
		# form_in_question = "4"
		# form_in_question = "8-k"
		self.ticker_query =  r'https://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK={}&filenum=&State=&Country=&SIC=&owner=exclude&Find=Find+Companies&action=getcompany'.format(co_seed)

	def get_master_files(self):
		for y in range(1994,2021):
			for q in range(1,5):
				file_path = './master_idx/q'+ str(q) + '_'+ str(y) + '_master.idx'
				url = self.sec_index_url + str(y) + "/QTR" + str(q) + "/master.idx"
				if not path.exists(file_path) or (path.exists(file_path) and os.path.getsize(file_path) == 0):
					num_new_files += 1
					r = requests.get(url)
					with open(file_path, 'w') as fp:
						fp.write(r.content.decode('iso-8859-1'))

				print('Number of new files: {}'.format(num_new_files))

	def get_co_data(self):
		if path.exists(file_path):
			with open(file_path,'r') as fp:
				for i in range(0,13):
					line = fp.readline()
				while line:
					cik_in_line = line.split('|')[0]
					
					if int(cik_text) != int(cik_in_line):
						line = fp.readline()
						continue
					if int(cik_text) == int(cik_in_line):
						if form_in_question.upper() == line.split('|')[2].upper():
							lines_in_question.append(self.filing_base_url + line.split('|')[4].replace('edgar/data','') \
									.replace('-','') \
									.replace('.txt','/index.json'))
					if int(cik_text) != int(cik_in_line) and len(lines_in_question) > 0:
						break
					line = fp.readline()

	def get_co_cik(self):
		r = requests.get(ticker_query)
		soup = BeautifulSoup(r.text, 'lxml')
		cik_text = soup.find('span', {'class':'companyName'}).find('a').text[:11]
	
	def get_co_filings(self):
		if inDoc:
			filing_form = map_to_filing(form_in_question)
			for item in lines_in_question:
				r = requests.get(item)
				theJson = json.loads(r.text)
				if theJson['directory']['name'] != "":
					url = sec_url + theJson['directory']['name']
					data_dir = theJson['directory']['name'].replace('/Archives/edgar/data','')
				
				for index, js in enumerate(theJson['directory']['item']):
					if filing_form.lower() in js['name'].lower():
						url += '/' + js['name']
# print('URL? {}'.format(url))
						break
				if form_in_question == "4":
					r = requests.get(url)
					proc_insider(r.text)
				elif form_in_question == "10-q":
					r = requests.get(url)
					print(proc_10_q(r.text, data_dir))
				elif form_in_question == "8-k":
					r = requests.get(url)
					proc_8_k(r.text)
		else: print("That was not found")

	def clean_up(self):
		qtr = "2"
		yr = "2019"

		path_to_idx = ""

		file_path = './master_idx/q{}_{}_master.idx'.format(qtr, yr)

		lines_in_question = []
		inDoc = True


	def proc_insider(self, web_text):
		soup = BeautifulSoup(web_text,'lxml')
		table = soup.find('table', {'class':'tableFile'})
		trs = table.find_all('tr')
		tds = trs[2].find_all('td')
		form_link = tds[2].find('a')['href']
		print(form_link)
		r = requests.get(sec_url +  form_link)
		xml_soup = BeautifulSoup(r.text,'lxml')
		buyer = xml_soup.find('ownershipdocument').find('reportingowner').find('reportingownerid').find('rptownername').text
		num_shares = xml_soup.find('ownershipdocument').find('nonderivativetable').find('transactionamounts').find('transactionshares').find('value').text
		trans_code = xml_soup.find('ownershipdocument').find('nonderivativetable').find('transactionamounts').find('transactionacquireddisposedcode').find('value').text 
		bought_sold = ("sold","bought")[trans_code == "A"]
		print('{} {} {} shares in this form'.format(buyer,bought_sold, num_shares))

	def proc_10_q(web_text, directory):
		root = ET.fromstring(web_text)
		exhibits_dict = {}
		for report in root.findall('./MyReports/Report'):
			if 'All Reports' != report.find('./ShortName').text:
				title = report.find('./ShortName').text
				filing_link = self.filing_base_url + directory + '/' + report.find('./HtmlFileName').text
# print('{}'.format(report.find('./ShortName').text))
# print('Filing link? [{}]'.format(filing_link))
				exhibits_dict[title] = filing_link
		return exhibits_dict
			
	def proc_8_k(web_text):
		soup = BeautifulSoup(web_text,'lxml')
		table = soup.find_all('table')
# print(table[0])

	def map_to_filing(self, form_in_question):
		forms = {'4':'form4',
			'8-k':'8-k',
			'10-q':'filingsummary'}

		return forms.get(form_in_question)

			
