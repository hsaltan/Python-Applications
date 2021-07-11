#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[2]:


webaddress="https://clutch.co/directory/mobile-application-developers"

r = requests.get(webaddress)

c = r.content

soup = BeautifulSoup(c, "html.parser")

page_nr = soup.find("li",{"class": "page-item last"}).find('a').get('data-page')

page_nr = int(page_nr)

print(page_nr)


# In[3]:


list_of_companies = []

base_url="https://clutch.co/directory/mobile-application-developers?page="

for page in range(page_nr):
    
    r = requests.get(base_url + str(page))
    
    c = r.content
    
    soup = BeautifulSoup(c,"html.parser")
    
    all_content = soup.find_all("li",{"class":"provider provider-row sponsor"})
    
    for item in all_content:
        
        company = {}
        
        companyName = item.find('h3').find('a').text
        
        locality = item.find("span",{"class":"locality"}).text
        
        minProjectSize = item.find("div",{"class":"list-item block_tag custom_popover"}).text.replace("\n", "")
        
        aveHourlyRate = item.find("div",{"class":"list-item custom_popover"}).text.replace("\n", "")
        
        employees = item.find("div", {"class":"list-item custom_popover"}).findNext('span').findNext('span').text

        company['Company Name'] = companyName
        
        company['Locality'] = locality
        
        company['No. of Employees'] = employees
        
        company['Min Project Size'] = minProjectSize
        
        company['Ave. Hourly Rate'] = aveHourlyRate
        
        list_of_companies.append(company)


# In[4]:


df = pd.DataFrame(list_of_companies)

df.head(10)

