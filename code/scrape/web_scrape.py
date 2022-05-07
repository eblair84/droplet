#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
# req = requests.get('https://www.barrons.com/articles/how-big-investors-use-your-personal-data-to-play-the-stock-market-1543627499?mod=article_signInButton')
req = requests.get('https://www.barrons.com/articles/capturing-our-anxious-times-in-google-search-51585353112?refsec=technology')
soup = BeautifulSoup(req.text,'html.parser')
# anchors = soup.find_all('data-module-id')
# anchors = soup.find_all(attrs={'data-module-id':'13'})
anchors = soup.find_all(attrs={'class':'snippet__buttons--subscribe primary-button'})
if not anchors:
    print("you can look at this")
    fp = open('/var/www/html/article.html','w+')
    fp.write(soup.prettify())
else:
    print(anchors)

'''for tag in anchors:
    printth("Tag: name [{}], text [{}], attribute [{}]".format(tag.name, tag.text, attribute))'''
