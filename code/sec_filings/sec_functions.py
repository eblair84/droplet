import requests, os, time, re, sys, argparse, pprint
import urllib
from bs4 import BeautifulSoup
from datetime import date, timedelta
import properties, time 

os.system('clear')
# sampleCo = sys.argv[1].upper()

def what_quarter(date):
    theDay = date # date.today()
    today = theDay - timedelta(days = 1)
    month = today.month
    return (month-1)//3+1

def create_url(base, parts):
    url = base

    for p in parts:
        url = '{}/{}'.format(url,p)

    return url

def get_text_from_site(url):
    r = requests.get(url)
    return r.text

def parse_to_components(url):
    return 'hello world'

sec_url = properties.sec_url

def search_too_broad(returned_text):
    return "Companies with names matching" in r.text

def no_company_found(returned_text):
    return "No matching companies" in r.text

def get_parsed_text(r):
    return BeautifulSoup(r.text,'lxml')

def get_cik(symbol):
    return requests.post("https://www.sec.gov/cgi-bin/cik_lookup",{'name':'pareteum'}).text

# print(get_cik('pareteum'))

base_url = r"https://www.sec.gov/Archives/edgar/daily-index" # properties.sec_url

year_url = create_url(base_url, ['2019','index.json'])

content = requests.get(year_url)
decoded_content = content.json()
pp = pprint.PrettyPrinter(indent=2)

# pp.pprint(decoded_content)
'''for item in decoded_content['directory']['item']:
    print('-'*100)

    print('Grabbing url for quarter {}'.format(item['name']))
    qtr_url = create_url(base_url,['2019',item['name'],'index.json'])
    print(qtr_url)
    file_content = requests.get(qtr_url)
    decoded_content = file_content.json()
    print('-'*100)
    for file in decoded_content['directory']['item']:
        file_url = create_url(base_url, ['2019',item['name'],file['name']])
        print(file_url)
    time.sleep(1)'''
file_url = r"https://www.sec.gov/Archives/edgar/daily-index/2019/QTR2/master.20190401.idx"

content = requests.get(file_url).content

with open('master_20190401.txt','wb') as fp:
    fp.write(content)
with open('master_20190401.txt','rb') as fp:
    byte_data = fp.read()

#Decode the byte data
data = byte_data.decode('utf-8').replace('\n','|').split('|')
'''for item in data:
    print("Item [{}]".format(item.replace('\n','')))
    time.sleep(1)'''

good_data_index = 0 
for index, item in enumerate(data):
    if "--" in item:
        good_data_index = index+1
        break
master_data = []
good_data = data[good_data_index:]
for index,company in enumerate(good_data):
    # print ('Item: [{}]'.format(company.replace('','')))
    if '.txt' in company:
        mini_list = good_data[(index -4): index + 1]
        if len(mini_list) > 0:
            mini_list[4] = 'https://www.sec.gov/Archives/' + mini_list[4]
            master_data.append(mini_list)
print(master_data[:3])
for index, doc in enumerate(master_data):
    document_dict = {}

    document_dict['cik_number'] = doc[0]
    document_dict['company_name'] = doc[1]
    document_dict['form_id'] = doc[2]
    document_dict['date'] = doc[3]
    document_dict['file_url'] = doc[4]
    master_data[index] = document_dict

play_company_url = ""
for doc_dict in master_data:
    if doc_dict['form_id'] == '10-K':
#         print(doc_dict['company_name'])
#        print(doc_dict['file_url'])
        if '1265107' in doc_dict['cik_number']:
            play_company_json = doc_dict['file_url'].replace('-','').replace('.txt','/index.json')
            play_company_htm = doc_dict['file_url'].replace('-','').replace('.txt','/index.html')
            break

print(play_company_htm)
print(play_company_json)
