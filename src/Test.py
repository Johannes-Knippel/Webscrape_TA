

import requests
import os
import tkinter as tk
import unicodedata

from tkinter import ttk
from bs4 import BeautifulSoup
from setuptools.package_index import HREF
from tinydb import TinyDB,Query,where





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
        
        for self.name in soup.find('h1', {'class': 'heading_title'}):
            print("Name:" + self.name.string)
        
        for self.rating_amount in soup.find('span', {'property': 'count'}):
            print("Anzahl Bewertungen:" + self.rating_amount.string)
            
        for self.popularity in soup.find_all('span', {'class': 'header_popularity popIndexValidation'}):
            print("Popularitaet:" + self.popularity.text)
        
        for self.price_level in soup.find('span', {'class': 'header_tags rating_and_popularity'}):
            print("Preis Level:" + self.price_level.string)
        
        for self.cuisine in soup.find_all('span', {'class': 'header_links rating_and_popularity'}):
            print('Kueche:' + self.cuisine.text)
        
        for self.contact_details in soup.find('div', {'class': 'blRow'}):
            print('Kontaktdaten:' + self.contact_details.text)
        
        for self.address in soup.find('span', {'class': 'street-address'}):
            print("Strasse:" + self.address.string)
    
        for self.locality in soup.find('span', {'class': 'locality'}):
            print("PLZ:" + self.locality.string)
        
        for self.phonenumber in soup.find_all('div', {'class': 'blEntry phone'}):
            print("Telefonnummer:" + self.phonenumber.text)
        
 
 


    '''
    Created on 18.04.2018
    
    @author: JohannesKnippel
    
    TinyDB - Database. Scraped Data from get_single_data() function will be parsed to a Database saved in .json-Format.
    '''
    #TinyDB
    def parse_to_tinydb(self):
        
        cwd = os.getcwd()
        try:
            #create the database or use the existing one
            db = TinyDB('db.json')
            #create the tables inside the database
            tableReviews = db.table('REVIEWS')
            tableUsers = db.table('USERS')
            tablePictures = db.table('PICTURES')
            tableRestaurants = db.table('RESTAURANTS')
        
        except:
            print("Error opening file")    
        
        
        
        #define the data to insert into database including an auto increment ID for each Table  
        
        
        #HANDLE REVIEWS
        #check if there already exists an entry in the REVIEWSs-table with the same name and the same address (these two attributes don't change/are not variable so there is a more constant way to check for duplicates)
#        if tableReviews.contains((where('++') == self.name.string) & (where('address') == self.address.string)): 
#            #pop up a message box
#            msg = "Dieses Hotel hast du bereits gesucht und ist in der Dtaenbak hinterlegt!"
#            popup = tk.Tk()
#            popup.wm_title("!")
#            label = ttk.Label(popup, text=msg)
#            label.pack(side="top", fill="x", pady=10)
#            B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
#            B1.pack()
#            popup.mainloop()
        # if there is no such entry, parse the data into the corresponding table of the database and define the data to insert into database including an auto increment ID for each Table       
#        else:
#            idReview =   
#            dataReviews = {'fruit':'orange', 'price':25}
#            tableReviews.insert(dataReviews)
        
        
        
        #HANDLE USERS
        #check if there already exists an entry in the USERS-table with the same name and the same address (these two attributes don't change/are not variable so there is a more constant way to check for duplicates)
#        if tableUsers.contains((where('name') == self.name.string) & (where('address') == self.address.string)): 
#            #pop up a message box
#            msg = "Dieses Hotel hast du bereits gesucht und ist in der Dtaenbak hinterlegt!"
#            popup = tk.Tk()
#            popup.wm_title("!")
#            label = ttk.Label(popup, text=msg)
#            label.pack(side="top", fill="x", pady=10)
#            B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
#            B1.pack()
#            popup.mainloop()
        # if there is no such entry, parse the data into the corresponding table of the database and define the data to insert into database including an auto increment ID for each Table       
#        else:
#            idUser = 
#            dataUsers = {'fruit':'orange', 'price':25}  
#            tableUsers.insert(dataUsers)
        
        
        
        #HANDLE PICTURES
        #check if there already exists an entry in the PICTURES-table with the same name and the same address (these two attributes don't change/are not variable so there is a more constant way to check for duplicates)
#        if tablePictures.contains((where('name') == self.name.string) & (where('address') == self.address.string)): 
#            #pop up a message box
#            msg = "Dieses Hotel hast du bereits gesucht und ist in der Dtaenbak hinterlegt!"
#            popup = tk.Tk()
#            popup.wm_title("!")
#            label = ttk.Label(popup, text=msg)
#            label.pack(side="top", fill="x", pady=10)
#            B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
#            B1.pack()
#            popup.mainloop()
        # if there is no such entry, parse the data into the corresponding table of the database and define the data to insert into database including an auto increment ID for each Table       
#        else:
#            idPicture =   
#            dataPictures = {'fruit':'orange', 'price':25} 
#            tableRestaurants.insert(dataRestaurants)
        
        
        
        #HANDLE RESTAURANTS
        #check if there already exists an entry in the Restaurans-table with the same name and the same address (these two attributes don't change/are not variable so there is a more constant way to check for duplicates)
        if tableRestaurants.contains((where('name') == self.name.string) & (where('address') == self.address.string)): 
            #pop up a message box
            msg = "Dieses Hotel hast du bereits gesucht und ist in der Dtaenbak hinterlegt!"
            popup = tk.Tk()
            popup.wm_title("!")
            label = ttk.Label(popup, text=msg)
            label.pack(side="top", fill="x", pady=10)
            B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
            B1.pack()
            popup.mainloop()
        # if there is no such entry, parse the data into the corresponding table of the database and define the data to insert into database including an auto increment ID for each Table       
        else:
            self.popularity2 = unicodedata.normalize("NFKD", self.popularity.text)
            self.idRestaurant = 1  
            dataRestaurants = {'id':self.idRestaurant, 'name':self.name.string, 'rating_amount':self.rating_amount.string, 'popularity':self.popularity2,'price_level':self.price_level.string, 'cuisine':self.cuisine.text, 'contact_details':self.contact_details.text, 'address':self.address.string, 'locality':self.locality.string, 'phonenumber':self.phonenumber.text}
            tableRestaurants.insert(dataRestaurants) 
        
        #################################bis hier 19.04.18###############
        # Idee: 4 tabellen mit drei IDs: Hotel_ID, User_ID, Review_ID
        # Implementieren dieser IDs per auto increment funktion.
      
      

            
        print(tableRestaurants.all())
        ft = Query()
        suche = tableRestaurants.search(ft.name == self.name.string)
        print(suche)         
            
        





# Main-function
# All functions are executed
ws = Web_scraping()
url = "https://www.tripadvisor.de/Restaurant_Review-g946452-d8757235-Reviews-The_Forge_Tea_Room-Hutton_le_Hole_North_York_Moors_National_Park_North_Yorkshire_.html"        
ws.get_single_data(url)
ws.parse_to_tinydb()

