import re
import requests
from bs4 import BeautifulSoup
from lxml import etree

for page in range(2, 4): # number of pages you want to Crawl
    markup = requests.get(f'https://unjobs.org/new/{page}').text
    soup = BeautifulSoup(markup, 'html.parser')
    counter = 1
    for item in soup.select('.job'):
        print ("un_jobs")
        print (item.find('a', class_='jtitle'))
        print (item.find_all('a .jtitle', href=True)[2].get('href'))


