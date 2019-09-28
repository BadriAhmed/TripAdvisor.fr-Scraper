#!/usr/bin/env python
# coding: utf-8

# ## Scraping TripAdvisor FR Reviews

# In[8]:


#import the libraries as needed
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import warnings
import pandas as pd
import numpy as np
warnings.filterwarnings("ignore")


# In[3]:


#Load urls and number of reviews to scrape
toscrape = pd.read_csv('toscrape.csv')


# In[4]:


# Store them into a list
urls,Nbr = [],[]
for index,row in toscrape.iterrows():
    urls.append(str(row['Url']))
    Nbr.append(int(row['NbCmnts']))


# In[6]:


reviews = []
ratelist = []


# In[9]:


for j in range (len(urls)):
    url = urls[j]
    Nb = Nbr[j]
    
        #using Chromedriver to open webpages without images
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome_options=chrome_options)
        #browser = webdriver.Chrome('chromedriver')
    #Headers will make it look like you are using a web browser
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    #We will use the iteration to retrieve and scrape the web pages, reviews, and ratings from each page on Trip Advisor
    for i in range(0,Nb,10):
        x=str(i)
        #Navigate to the next page
        url = url.replace('Review','Review-or'+x)
        browser.get(url)
        time.sleep(5)
        element_list = browser.find_elements_by_xpath("//span[@class='taLnk ulBlueLinks']")
        #Iteration clicks all of the 'More' links. The 'try' statement allows the iteration 
        #to continue with 'pass' when an error message appears-caused by TA.
        for e in element_list:
            try:
                e.click()
            except:
                pass
            #Variable to get the page source through BeautifulSoup.
        html = browser.page_source
        response = requests.get(url, headers=headers, verify=False).text
        soup = BeautifulSoup(response)
    #Looping through 'div' 'reviewSelector' will help find all the review containers we need in each page that have rating and review
        for r in soup.find_all('div', 'reviewSelector'):
            rating = int(r.find('span','ui_bubble_rating')['class'][1].split('_')[1])/10
            review = r.p.text
    #Cleaning the lemmas or words in reviews now will make it easier when we start predictive modeling

            reviews.append(review)
    #Here we are using a simple control flow to recode the ratings for our model. If rating is 1-3 negative, else positive

            ratelist.append(rating)
        print(i+10,' Comments have been collected')
    browser.quit()
    print("Url nbr ",j+1,' Scraped successfully')
print("Finished!")


# In[8]:


data = pd.DataFrame({'Comment':reviews,
                    'Rate':ratelist})


# In[9]:


data.head()


# In[ ]:




