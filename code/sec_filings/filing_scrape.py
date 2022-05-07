import requests
import pandas as pd
from bs4 import BeautifulSoup

base_url = r"https://sec.gov"
documents_url = r"https://www.sec.gov/Archives/edgar/data/1265107/000126510719000004/index.json"

content = requests.get(documents_url).json()

for file in content['directory']['item']:
    if file['name'] == 'FilingSummary.xml':
        xml_summary = base_url + content['directory']['name'] + "/" + file['name']
        print('-' * 100)
        print('File Name: ' + file['name'])
        print('File Path: ' + xml_summary)

base_url = xml_summary.replace('FilingSummary.xml','')

content = requests.get(xml_summary).content

soup = BeautifulSoup(content,'lxml')

reports = soup.find('myreports')

master_reports = []

for report in reports.find_all('report')[:-1]:
    # let's create a dictionary to store all the different parts we need.
    report_dict = {}
    report_dict['url'] = base_url + report.htmlfilename.text
    report_dict['name_long'] = report.longname.text
    report_dict['name_short'] = report.shortname.text
    report_dict['category'] = report.menucategory.text
    report_dict['position'] = report.position.text
    
    # append the dictionary to the master list.
    master_reports.append(report_dict)
    
    # print the info to the user.
    print('-'*100)
    print(base_url + report.htmlfilename.text)
    print(report.longname.text)
    print(report.shortname.text)
    print(report.menucategory.text)
    print(report.position.text)
    
    statements_url = []
    
for report_dict in master_reports:
    # define the statements we want to look for.
    item1 = r"Consolidated Balance Sheets"
    item2 = r"Consolidated Statements of Operations and Comprehensive Income (Loss)"
    item3 = r"Consolidated Statements of Cash Flows"
    item4 = r"Consolidated Statements of Stockholder's (Deficit) Equity"
    
    # store them in a list.
    report_list = [item1, item2, item3, item4]
    
    # if the short name can be found in the report list.
    if report_dict['name_short'] in report_list:
            
        # print some info and store it in the statements url.
        print('-'*100)
        print(report_dict['name_short'])
        print(report_dict['url'])
        
        statements_url.append(report_dict['url'])
            
statements_data = []
            
# loop through each statement url
for statement in statements_url:
    # define a dictionary that will store the different parts of the statement.
    statement_data = {}
    statement_data['headers'] = []
    statement_data['sections'] = []
    statement_data['data'] = []
    # request the statement file content
    content = requests.get(statement).content
    report_soup = BeautifulSoup(content, 'html.parser')
    # find all the rows, figure out what type of row it is, parse the elements, and store in the statement file list.
    for index, row in enumerate(report_soup.table.find_all('tr')):
        cols = row.find_all('td')
        
        # if it's a regular row and not a section or a table header
        if (len(row.find_all('th')) == 0 and len(row.find_all('strong')) == 0): 
            reg_row = [ele.text.strip() for ele in cols]
            statement_data['data'].append(reg_row)
            
            # if it's a regular row and a section but not a table header
        elif (len(row.find_all('th')) == 0 and len(row.find_all('strong')) != 0):
            sec_row = cols[0].text.strip()
            statement_data['sections'].append(sec_row)
            
            # finally if it's not any of those it must be a header
        elif (len(row.find_all('th')) != 0):            
            hed_row = [ele.text.strip() for ele in row.find_all('th')]
            statement_data['headers'].append(hed_row)
            
        else:            
            print('We encountered an error.')
            
            # append it to the master list.
    statements_data.append(statement_data)
# Grab the proper components
income_header =  statements_data[1]['headers'][1]
income_data = statements_data[1]['data']

# Put the data in a DataFrame
income_df = pd.DataFrame(income_data)

# Display
print('-'*100)
print('Before Reindexing')
print('-'*100)
display(income_df.head())

# Define the Index column, rename it, and we need to make sure to drop the old column once we reindex.
income_df.index = income_df[0]
income_df.index.name = 'Category'
income_df = income_df.drop(0, axis = 1)

# Display
print('-'*100)
print('Before Regex')
print('-'*100)
display(income_df.head())

# Get rid of the '$', '(', ')', and convert the '' to NaNs.
income_df = income_df.replace('[\$,)]','', regex=True )\
                     .replace( '[(]','-', regex=True)\
                     .replace( '', 'NaN', regex=True)

# Display
print('-'*100)
print('Before type conversion')
print('-'*100)
display(income_df.head())

# everything is a string, so let's convert all the data to a float.
income_df = income_df.astype(float)

# Change the column headers
income_df.columns = income_header

# Display
print('-'*100)
print('Final Product')
print('-'*100)

# show the df
income_df

# drop the data in a CSV file if need be.
# income_df.to_csv('income_state.csv')'''
