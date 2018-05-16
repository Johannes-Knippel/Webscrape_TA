# -*- coding: utf-8 -*-

import requests
import os
import unicodedata
import validators
import threading
import json

from tkinter import *
from tkinter import messagebox
import tkinter as tk
import tkinter as ttk

from bs4 import BeautifulSoup
from setuptools.package_index import HREF
from tinydb import TinyDB,Query,where





class Web_scraping:
    
    '''
    Created on 17.04.2018
    
    @author: anjawolf
    
    get_single_data: Data will be scraped from the Tripadvisors Website and stored in variables.
    '''
    #scrape the restaurant data from the given URL and store it in a db
    def get_single_data(self,url):
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        
        self.name = soup.find('h1', {'class': 'heading_title'})
        print("Restaurantname: " + self.name.string)
            
        self.overallPoints = soup.find('div', {'class':'rs rating'})
        print ("Punkteskala: " + self.overallPoints.div.span['content'])
        
        for self.rating_amount in soup.find('span', {'property': 'count'}):
            print("Anzahl_Bewertungen: " + self.rating_amount.string)
            
        for self.popularity in soup.find_all('span', {'class': 'header_popularity popIndexValidation'}):
            print("Popularitaet: " + self.popularity.text)
        
        for self.price_level in soup.find('span', {'class': 'header_tags rating_and_popularity'}):
            print("Preis_Level: " + self.price_level.string)
        
        for self.cuisine in soup.find_all('span', {'class': 'header_links rating_and_popularity'}):
            print('Kueche: ' + self.cuisine.text)
        
        for self.address in soup.find('span', {'class': 'street-address'}):
            print("Strasse: " + self.address.string)
    
        for self.locality in soup.find('span', {'class': 'locality'}):
            print("PLZ_Ort: " + self.locality.string)
        
        for self.phonenumber in soup.find_all('div', {'class': 'blEntry phone'}):
            print("Telefonnummer: " + self.phonenumber.text)

        #
        #load all relevant restaurant data into database (table: RESTAURANTS)    
        self.parse_to_tinydb_rest()   
        #       
        #


        #get all the review containers from current page
        review_containers = soup.find_all('div', class_= 'review-container')
        reviewsPerPage = len(review_containers)

        
        #get the pageNumbers for all reviews per restaurant
        pageNumbers = soup.find_all('a', class_= 'pageNum')
        pages = len(pageNumbers)
        counter = 1
        
        #Extract data from single containers   
        for container in review_containers:
                
            for link in container.find_all('a', href=True):
                href = "https://www.tripadvisor.de" + str(link.get('href'))
                #pass it to the function where single data is scraped
                self.get_single_review_data(href)
                counter = counter + 1
                
        
        #create a new_url for each page of the reviews
        for index in range (10,pages*10, 10):
            
            data = url.split("Reviews-")
            new_url = data[0]+"Reviews-or"+str(index)+'-'+data[1]
            #pass the new_url to the loop_trough_review_pages function
            self.loop_through_review_pages(new_url)
        
        print ("Es wurden " + str(counter) + " textuelle von " + self.rating_amount.string + " Bewertungen abgegeben!")
     
        


    #loop through the restaurant review pages
    def loop_through_review_pages(self, loop_url):
        
        source_code = requests.get(loop_url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        
        #get all review containers but on the nuw_url
        review_containers = soup.find_all('div', class_= 'review-container')
        reviewsPerPage = len(review_containers)
        
        #search trough all reviews on the page
        for container in review_containers:
                
            for link in container.find_all('a', href=True):
                href = "https://www.tripadvisor.de" + str(link.get('href'))
                #pass it to the function where single data is scraped
                self.get_single_review_data(href)

    


    #loop through the reviews and scrape the data
    def get_single_review_data(self,review_url):
            
        source_code2 = requests.get(review_url)
        plain_text2 = source_code2.text
        soup = BeautifulSoup(plain_text2, "html.parser")
        
        #Lists to store scraped data in
        self.username = soup.find('span', {'class': 'expand_inline scrname'}).text
        print('Username: ' + self.username)
        
        for self.numberOfReviews in soup.findAll('span', {'class': 'badgetext'})[0]:
            print("Number of reviews: " + self.numberOfReviews.string)
            
            
        for self.numberOfLikes in soup.findAll('span', {'class': 'badgetext'})[1]:
            print("Number of likes: " + self.numberOfLikes.string)

        #intizialise and load the json from TA to search for relevant data     
        self.item_name = soup.find('script', {'type': 'application/ld+json'})
        json_string = str(self.item_name.string)
        obj = json.loads(json_string)
        
        #get title of the review
        self.title = obj["name"]
        print ("Titel: " + self.title)
        
        #get content of the review
        self.review = obj["reviewBody"]
        print ("Bewertung: " + self.review)

        #get rating of the review    
        self.points = soup.find('div', {'class':'rating'})
        print ("Rating: "+ self.points.span.span['alt'].split()[0])

        #Get URL from review pictures
        for link in soup.findAll('img', {'class': 'centeredImg'}):
            self.src = link.get('src')
            print("source of picture: " + self.src)
 
    
    


    '''
    Created on 18.04.2018
    
    @author: JohannesKnippel
    
    TinyDB - Database. Scraped Data from get_single_data() function will be parsed to a Database saved in .json-Format.
    '''

    def endProgram(self):
        exit()


    #TinyDB
    def parse_to_tinydb_rest(self):
        
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
        
        #################################bis hier 19.04.18###############
        # Idee: 4 tabellen mit drei IDs: Hotel_ID, User_ID, Review_ID
        # Implementieren dieser IDs per auto increment funkkion.
        
        #define the data to insert into database including an auto increment ID for each Table  

        #HANDLE RESTAURANTS
        #check if there already exists an entry in the Restaurans-table with the same name and the same address (these two attributes don't change/are not variable so there is a more constant way to check for duplicates)
        if tableRestaurants.contains((where('RESTAURANTNAME') == self.name.string) & (where('PLZ_ORT') == self.locality.string)): 
            #pop up a message box
            msg = "Dieses Hotel hast du bereits gesucht und ist in der Datenbank hinterlegt!"
            popup = tk.Tk()
            popup.wm_title("!")
            label = ttk.Label(popup, text=msg)
            label.pack(side="top", fill="x", pady=10)
            B1 = ttk.Button(popup, text="Okay und Beenden", command = self.endProgram)
            B1.pack()
            popup.mainloop()
        # if there is no such entry, parse the data into the corresponding table of the database and define the data to insert into database including an auto increment ID for each Table       
        else:
            self.name2 = unicodedata.normalize("NFKD", self.name.string)
            self.popularity2 = unicodedata.normalize("NFKD", self.popularity.text)
            self.cuisine2 = unicodedata.normalize("NFD", self.cuisine.text)
            self.address2 = unicodedata.normalize("NFKD", self.address.string)
            self.price_level2 = unicodedata.normalize("NFKC", self.price_level.string)
            self.idRestaurant = 1  
            dataRestaurants = {'ID':self.idRestaurant, 'RESTAURANTNAME':self.name2, 'PUNKTESKALA':self.overallPoints.div.span['content'], 'ANZAHL_BEWERTUNGEN':self.rating_amount.string, 'POPULARITAET':self.popularity2, 'PREIS_LEVEL':self.price_level2, 'KUECHE':self.cuisine2, 'STRASSE':self.address2, 'PLZ_ORT':self.locality.string, 'TELEFONNUMMER':self.phonenumber.text}
            tableRestaurants.insert(dataRestaurants) 
        
        
                  
        print(tableRestaurants.all())
        ft = Query()
        suche = tableRestaurants.search(ft.name == self.name.string)
        print(suche) 


    def parse_to_tinydb_us_rev_pic(self):
        print("Hello")
        
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
         #if there is no such entry, parse the data into the corresponding table of the database and define the data to insert into database including an auto increment ID for each Table       
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
        #if there is no such entry, parse the data into the corresponding table of the database and define the data to insert into database including an auto increment ID for each Table       
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








        
    '''
    @author: Skanny Morandi
   
    opens a GUI that validates a given url-string and starts the scraping on button click
    '''

    def start_GUI(self):

        roots = Tk()
        roots.title('Tripadvisor Scraper')
        instruction = Label(roots, text='Please provide Restaurant-Url\n')
        instruction.grid(row=0, column=0, sticky=E)

        restaurant_label = Label(roots, text='Restaurant-URL ')
        restaurant_label.grid(row=1, column=0, sticky=W)

        restaurant_entry = Entry(roots, width=150)

        restaurant_entry.grid(row=1, column=1)

        def check_url():
            base_restaurant_url_= "https://www.tripadvisor.de/Restaurant_Review"
            url_to_check = restaurant_entry.get()
            if  (not validators.url(url_to_check)) or \
                (base_restaurant_url_ not in url_to_check):

                messagebox.showwarning("Warning", "This seems not to be valid Tripadvisor restaurant URL")

            else:
                messagebox.showinfo("Vaildation successful", "Url seems to be valid")


        check_url_Button= Button(roots, text='Validate Url', command=check_url)

        def go_scrape():
            self.get_single_data(restaurant_entry.get())

        scrape_button = Button(roots, text='Go Scrape', command=go_scrape)

        check_url_Button.grid(columnspan=3, sticky=W)
        scrape_button.grid(columnspan=5, sticky=W)
    
        roots.mainloop()

           

if __name__ == "__main__":
    ws = Web_scraping()
    ws.start_GUI()

    #url = "https://www.tripadvisor.de/Restaurant_Review-g946452-d8757235-Reviews-The_Forge_Tea_Room-Hutton_le_Hole_North_York_Moors_National_Park_North_Yorkshire_.html"



