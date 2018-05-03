

import requests
import os
import unicodedata
import validators
from tkinter import *
from tkinter import messagebox

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
            
            
            
        
        
        #get all the review containers from current page
        review_containers = soup.find_all('div', class_= 'review-container')
        reviewsPerPage = len(review_containers)
        #print (reviewsPerPage)
        
        #get the pageNumbers for all reviews per restaurant
        pageNumbers = soup.find_all('a', class_= 'pageNum')
        pages = len(pageNumbers)
        
        #Extract data from single containers   
        for container in review_containers:
                
            for link in container.find_all('a', href=True):
                href = "https://www.tripadvisor.de" + str(link.get('href'))
                #pass it to the function where single data is scraped
                self.get_single_review_data(href)
        
        #create a new_url for each page of the reviews
        for index in range (10,pages*10, 10):
            
            data = url.split("Reviews-")
            new_url = data[0]+"Reviews-or"+str(index)+'-'+data[1]
            #print(new_url)
            #pass the new_url to the loop_trough_review_pages function
            self.loop_through_review_pages(new_url)
    
    
    
    
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
                
    
    
    
    def get_single_review_data(self,review_url):
            
        source_code2 = requests.get(review_url)
        plain_text2 = source_code2.text
        soup = BeautifulSoup(plain_text2, "html.parser")
        
        #Lists to store scraped data in
        
        usernames = []
        noReviews = []
        titles = []
        content = []
        ratings = []
        
        self.titles = soup.find('div', {'id': 'PAGEHEADING'}).text
        titles.append(self.titles)
        #print('Titel:' + self.title.text)
        
        self.content = soup.find('p', {'class': 'partial_entry'}).text
        content.append(self.content)
        
        self.usernames = soup.find('span', {'class': 'expand_inline scrname'}).text
        usernames.append(self.usernames)
        
        self.noReviews = soup.find('div', {'class:': 'memberBadgingNoText'})
        noReviews.append(self.noReviews)
        
        self.rating = soup.find('span', 'alt')
        #print(self.rating)
        
        print(usernames)
        #print(noReviews)
        print(titles)
        print(content)
        print(review_url)
       
       
       #print(first_link)
        #titel = soup.find('p', {'class': 'entry'})
       
        '''
        @author: JohannaSickendiek
       
        '''
       #Get the whole text of the review
        #for self.item_name in soup.find('p'):
         #   print(self.item_name.string)
        
        for self.item_name in soup.findAll('script', {'type': 'application/ld+json'}):
            print(self.item_name.string)
            
        
        #1. Moeglichkeit
       # for self.item_name in soup.find('p', {'class': 'partial_entry'}):
        #    print(self.item_name.string)
        
        # 2. Moeglichkeit
       # table = soup.findAll('div',attrs={"class":"partial_entry"})
        #for review in table:
         #   print(review.find('p').text)
        
        #Get URL from review pictures
        for link in soup.findAll('img', {'class': 'centeredImg'}):
            self.src = link.get('src')
            print("source of picture: " + self.src)
 


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
        restaurant_label.grid(row=1, column=0,
                             sticky=W)

        restaurant_entry = Entry(roots, width=100)

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

        check_url_Button.grid(columnspan=2, sticky=W)
        scrape_button.grid(columnspan=3, sticky=W)

        roots.mainloop()

if __name__ == "__main__":
    ws = Web_scraping()
    ws.start_GUI()
    #ws.parse_to_tinydb()

    #url = "https://www.tripadvisor.de/Restaurant_Review-g946452-d8757235-Reviews-The_Forge_Tea_Room-Hutton_le_Hole_North_York_Moors_National_Park_North_Yorkshire_.html"
    #ws.get_single_data(url)




# Main-function
# All functions are executed
#ws = Web_scraping()
        
#ws.get_single_data(url)
#ws.parse_to_tinydb()

