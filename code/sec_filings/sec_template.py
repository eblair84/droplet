import requests, os, time, re, sys
import urllib
from bs4 import BeautifulSoup
from datetime import date, timedelta
import properties

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


# dataUrl = 'https://www.sec.gov/cgi-bin/browse-edgar?company=pareteum&owner=include&action=getcompany'
sec_url = properties.base_url
dataUrl = 'https://www.sec.gov/cgi-bin/browse-edgar?company=pareteum&owner=include&action=getcompany&count=100'
# dataUrl = 'https://www.sec.gov/Archives/edgar/daily-index/' + str(today.year) + '/QTR' + str(qtr) + '/'
filingUrl = 'https://www.sec.gov/Archives/'
r = requests.get(dataUrl)
i = 1
while True:
    nextPageUri = ""
    if "Companies with names matching" in r.text:
        print("More than one company came up in that search")
    hasData = True
    if "No matching companies" in r.text:
        print("There were no matching company data found for this query")
        hasData = False

    soup = BeautifulSoup(r.text, 'lxml')

    # patternToFind = ''.join(["crawler.", str(today).replace('-','')])
    links = soup.find_all("a") # , href=re.compile(patternToFind))

    filingTable = soup.find("table", class_="tableFile2")

    filingHeader = filingTable.find_all("th")


    coInfo = soup.find('p', class_='identInfo')
    prevCos = coInfo.find_all(text=re.compile('formerly'))
    for co in prevCos:
        print("Previous Co name: [{}]".format(co))
#    time.sleep(2)

    for head in filingHeader:
        print("Header: [{}]".format(head.text))
    #time.sleep(2)
    filingRow = filingTable.find_all("tr")
    if len(filingRow) == 1:
        print("There is no data available for this query")
# UNCOMMENT THIS ONCE PAGING IS DONE
    for filing in filingRow:
        print("Filing: [{}]".format(filing))
#    time.sleep(2)
    # sampleCo = 'ABERCROMBIE'
    next100 = soup.find_all('input', {'type':'button','value':'Next 100'})
    if len(next100) > 0:
        nextPageUri = next100[0]['onclick'][len('parent.location=\''):-1]
#        time.sleep(4)
        morePages = True
    else:
        print("More pages is false?")
        morePages = False
    #UNCOMMENT THIS ONCE PAGING IS DONE TESTING
    for link in links:
        print(link.text)

        
    if morePages:
        nextUrl = 'https://www.sec.gov' + nextPageUri 
        print("Next URL: [{}]".format(nextUrl))
        i += 1
        r = requests.get(nextUrl)
        print("More pages at end!!") 
        print("i = [{}]".format(i))
        #time.sleep(2)
    else:
        print("We're done. Page number is [{}]".format(i*100))
        break
    '''day =  link.get('href')
        if "getcompany" in day:
            print("Action for the URL: [{}]".format(day))
        else:
            print(day)'''


    ''' Data format [company.date.idx]'''
    '''    if 'crawler.' in day:
            allCos = requests.get(dataUrl + day,stream=True)
            for line in allCos.iter_lines():
                filing = line.decode('utf-8')
                filing = re.sub('  +',',',filing)
                parts = filing.split(',')
                if sampleCo in parts[0]:
                    print("[{}], CIK: [{}] filed [{}] with the SEC on [{}], link: [{}]"'''
