

import requests
import os


from bs4 import BeautifulSoup
from setuptools.package_index import HREF
from tinydb import TinyDB,Query





class Web_scraping:
    
    '''
    Created on 17.04.2018
    
    @author: anjawolf
    
    get_single_data: Data will be scraped from the Tripadvisors Website and stored in variables.
    '''
    def get_single_data(self,url):
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        
        for self.item_name in soup.find_all('h1', {'class': 'heading_title'}):
            print("Name:" + self.item_name.string)
            
        for self.rating_amount in soup.find_all('span', {'property': 'count'}):
            print("Anzahl Bewertungen:" + self.rating_amount.string)
            
        for self.price_level in soup.find_all('span', {'class': 'header_tags rating_and_popularity'}):
            print("Preis Level:" + self.price_level.string)
            
        for self.item_address in soup.find_all('span', {'class': 'street-address'}):
            print("Straße:" + self.item_address.string)
        
        for self.item_locality in soup.find_all('span', {'class': 'locality'}):
            print("PLZ:" + self.item_locality.string)
            
        ##for item_number in soup.find_all('span'):
           ## print("Telefonnummer:" + item_number.string)
            
        for link in soup.find_all('a'):
            href = link.get('href')
            print(href)
        
 
 


    '''
    Created on 18.04.2018
    
    @author: JohannesKnippel
    
    TinyDB - Database. Scraped Data from get_single_data() function will be parsed to a Database saved in .json-Format.
    '''
    #TinyDB
    def parse_to_tinydb(self):
        cwd = os.getcwd()
        print(cwd)
        data = {}
        data['people'] = []
        data['people'].append({ 
            'name': 'Hans',
            'website': 'bierdimpfe.bavaria',
            'from': 'Heppala'
        })
        try:
             with open(os.path.join(cwd, "db.json"), "w") as outfile:
                 json.dump(data, outfile)
 
        
        except:
            print("Error opening file")     
                  
        
        print(self.item_name.string)       
        





# main-function
# All functions are executed
ws = Web_scraping()
url = "https://www.tripadvisor.de/Restaurant_Review-g504000-d720608-Reviews-Star_Inn-Harome_North_Yorkshire_England.html"        
ws.get_single_data(url)
ws.parse_to_tinydb()



















