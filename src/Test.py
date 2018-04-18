'''
Created on 17.04.2018

@author: anjawolf
'''

import requests

from bs4 import BeautifulSoup
from setuptools.package_index import HREF


def get_single_data(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    
    for item_name in soup.find_all('h1', {'class': 'heading_title'}):
        print("Name:" + item_name.string)
        
    for rating_amount in soup.find_all('span', {'property': 'count'}):
        print("Anzahl Bewertungen:" + rating_amount.string)
        
    for price_level in soup.find_all('span', {'class': 'header_tags rating_and_popularity'}):
        print("Preis Level:" + price_level.string)
        
    for item_address in soup.find_all('span', {'class': 'street-address'}):
        print("Straße:" + item_address.string)
    
    for item_locality in soup.find_all('span', {'class': 'locality'}):
        print("PLZ:" + item_locality.string)
        
    ##for item_number in soup.find_all('span'):
       ## print("Telefonnummer:" + item_number.string)
        
    for link in soup.find_all('a'):
        href = link.get('href')
        print(href)
        
        
        
 
url = "https://www.tripadvisor.de/Restaurant_Review-g504000-d720608-Reviews-Star_Inn-Harome_North_Yorkshire_England.html"        
get_single_data(url)