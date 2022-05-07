import requests, os, time, re, sys
from bs4 import BeautifulSoup
from datetime import date, timedelta

os.system('clear')
sampleCo = sys.argv[1].upper()
theDay = date.today()
today = theDay - timedelta(days = 1)
month = today.month
qtr = (month-1)//3+1

dataUrl = 'https://www.sec.gov/Archives/edgar/daily-index/' + str(today.year) + '/QTR' + str(qtr) + '/'
filingUrl = 'https://www.sec.gov/Archives/'
r = requests.get(dataUrl)

soup = BeautifulSoup(r.text, 'lxml')

patternToFind = ''.join(["crawler.", str(today).replace('-','')])
links = soup.find_all("a" , href=re.compile(patternToFind))
# sampleCo = 'ABERCROMBIE'

for link in links:
    day =  link.get('href')
    ''' Data format [company.date.idx]'''
    if 'crawler.' in day:
        allCos = requests.get(dataUrl + day,stream=True)
        for line in allCos.iter_lines():
            filing = line.decode('utf-8')
            filing = re.sub('  +',',',filing)
            parts = filing.split(',')
            if sampleCo in parts[0]:
                print("[{}], CIK: [{}] filed [{}] with the SEC on [{}], link: [{}]"
                        .format(parts[0], parts[1],parts[2],parts[3],parts[4]))
