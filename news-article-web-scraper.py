#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests 
from bs4 import BeautifulSoup 
import pandas as pd
import re


# In[69]:


all_daily_links = []

curr_year = 2010
curr_month = 1
curr_day = 1
curr_offset = 40178

months1 = [1,3,5,7,8,10,12]
months2 = [4,6,9,11]
months3 = [2]

leap_years = [2012,2016]

while curr_offset < 43428:
    all_article_links = []
    
    curr_url = "https://timesofindia.indiatimes.com/"+str(curr_year)+"/"+str(curr_month)+"/"+str(curr_day)+"/archivelist/year-"+str(curr_year)+",month-"+str(curr_month)+",starttime-"+str(curr_offset + 1)+".cms"
    
    print(curr_url)
    
    all_daily_links.append(curr_url)
    
    r = requests.get(curr_url) 
    soup = BeautifulSoup(r.content, 'html5lib') 

    all_links = soup.find_all('a')

    for link in all_links:
        match = re.search(r'http://timesofindia.indiatimes.com//.*\.cms', str(link))
        if match:
            all_article_links.append(match.group(0))
    
    if curr_month == 12 and curr_day == 31:
            curr_year = curr_year + 1
            curr_month = 1
            curr_day = 1
    elif curr_month in months1 and curr_day == 31:
        curr_month = curr_month + 1
        curr_day = 1
    elif curr_month in months2 and curr_day == 30:
        curr_month = curr_month + 1
        curr_day = 1
    elif curr_month in months3:
        if curr_year in leap_years and curr_day == 29:
                curr_month = curr_month + 1
                curr_day = 1
        elif curr_year not in leap_years and curr_day == 28:
                curr_month = curr_month + 1
                curr_day = 1
        else:
            curr_day = curr_day + 1
    else:
        curr_day = curr_day + 1
    
    curr_offset = curr_offset + 1


# In[ ]:




