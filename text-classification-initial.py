
# coding: utf-8

# In[1]:


# imports
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances
import collections
from rake_nltk import Rake
import re
import pandas as pd
import pymysql
from nltk.stem.lancaster import LancasterStemmer
import os
import json
import datetime
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

stemmer = LancasterStemmer()


# In[2]:


# connect to database
connection = pymysql.connect(host='localhost',
                             user='root',
                             db='news_article_analysis')
cursor = connection.cursor()


# In[3]:


# create document matrix for manually classified data

classes = [0,1,2,3,4,5,6,7,8,9]
processed_documents = []

for _class in classes:
    query = "SELECT `title` FROM articles WHERE class = \""+str(_class)+"\" AND sr_no < 901"
    cursor.execute(query)
    article_fetch = cursor.fetchall()
    processed_string = ""
    for article in article_fetch:
        r = Rake(language='english')
        r.extract_keywords_from_text(article[0])
        tags = r.get_ranked_phrases()
        for tag in tags:
            tokens = set(word_tokenize(tag))
            for token in tokens:
                curr_tag = stemmer.stem(token)
                if curr_tag not in processed_string:
                    processed_string += curr_tag + " "
    processed_documents.append(processed_string)


# In[3]:


processed_documents = []
processed_string = ""
deaths = "killed beaten death burned mortal"
r = Rake(language='english')
r.extract_keywords_from_text(deaths)
tags = r.get_ranked_phrases()
for tag in tags:
    tokens = set(word_tokenize(tag))
    for token in tokens:
        curr_tag = stemmer.stem(token)
        if curr_tag not in processed_string:
            processed_string += curr_tag + " "
processed_documents.append(processed_string)
            
processed_string = ""
suicide = "jumped hanged commits suicide self himself herself"
r = Rake(language='english')
r.extract_keywords_from_text(suicide)
tags = r.get_ranked_phrases()
for tag in tags:
    tokens = set(word_tokenize(tag))
    for token in tokens:
        curr_tag = stemmer.stem(token)
        if curr_tag not in processed_string:
            processed_string += curr_tag + " "
processed_documents.append(processed_string)


# In[4]:


query = "SELECT * FROM `articles` WHERE sr_no > 901"
cursor.execute(query)
new_article_fetch = cursor.fetchall()
for new_article in new_article_fetch:
    final_score = 0
    class_ = 0
    r = Rake(language='english')
    processed_string = ""
    r.extract_keywords_from_text(new_article[5])
    tags = r.get_ranked_phrases()
    for tag in tags:
        tokens = set(word_tokenize(tag))
        for token in tokens:
            curr_tag = stemmer.stem(token)
            if curr_tag not in processed_string:
                processed_string += curr_tag + " "
    for x in range(len(processed_documents)):
        tfidf_vectorizer = TfidfVectorizer(ngram_range = (0,1))
        train_set = [processed_documents[x], processed_string]
        tfidf_train = tfidf_vectorizer.fit_transform(train_set)
        score = cosine_similarity(tfidf_train[0:1],tfidf_train)[0][1]
        if score > final_score:
            final_score = score
            class_ = x
        #print(score)
    if class_ != 0:
        print(new_article[5] + " : " + str(class_))

