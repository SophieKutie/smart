#!/usr/bin/env python
# coding: utf-8

# In[2]:


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API as api
from tweepy import Cursor
import tweepy
import time
import datetime
from datetime import datetime
import json
import pandas as pd
import matplotlib.pyplot as plt
import re
import os, sys
import pprint
import math
import random
import csv

# In[4]:


'''
get a list of hateful terms. These ae collected from hatebase.org using the hatespeech-vocabulary-collection script 
stroed in hatespeech-terms.csv file
csv_file_name should include the full path to the file
the file should be formatted as one column labelled 'term' and as many terms as required

term
term 1
term 2
term 3
...
'''


def get_hate_terms(csv_file_name):
    terms = pd.read_csv(csv_file_name, encoding='utf')
    # terms.sort_values('term', inplace=True)
    # print('Before removing duplicated terms: ', terms.count())
    terms.drop_duplicates(keep='first', inplace=True)
    # print('After removing duplicated terms: ',  terms.count())
    return terms['terms'].astype(str).values.tolist()


# hate_terms = get_hate_terms('./data/abusive_terms.csv')
cons = get_hate_terms('./test/data/abusive_terms.csv')
ind = get_hate_terms('./test/data/abusive_terms.csv')
labour = get_hate_terms('./test/data/abusive_terms.csv')
lib_dem = get_hate_terms('test/data/abusive_terms.csv')

terms = cons + ind + labour + lib_dem

'''
Twitter only accepts n number of terms at a time
Use this function if we have a large number of terms so we supply twitter with small list of terms in each API call
return randomised list of terms
'''


def get_list_of_list(list_of_terms, sublist_size):
    random_list = random.sample(list_of_terms, len(list_of_terms))
    # print(random_list)
    # For item i in a range that is a length of l,
    for i in range(0, len(random_list), sublist_size):
        # Create an index range for l of n items:
        yield random_list[i:i + sublist_size]


term_list = list(get_list_of_list(terms, 99))
print('The number of list terms to be processed: %d' % len(term_list))
for terms in term_list:
    print(terms)


def get_start_time():
    start_time = time.time()
    print('started at: ', datetime.fromtimestamp(start_time).strftime("%c"))
    return start_time


def get_time_taken(start_time):
    end_time = time.time()
    print('ended at: ', datetime.fromtimestamp(end_time).strftime("%c"))
    total_time_taken = end_time - start_time
    total_time_taken = datetime.fromtimestamp(total_time_taken)
    print('time taken: ', total_time_taken.strftime('%M'), ':', total_time_taken.strftime('%S'), ' seconds')


# from TwitterAPI import TwitterRestPager
# from t import TwitterRestPager

SEARCH_TERM = 'pizza'
GEOCODE = '40,74,10km'
cons = get_hate_terms('./data/conservative.csv')

for tweet in tweepy.Cursor(api.search, q=SEARCH_TERM, count=100, lang="en", since="2019-12-09",
                           until="2019-12-15").items():
    print(tweet)
# In[3]:


accesstoken = '98886733-f5M5aYz2w3zivEILEHuFfvrDLXhYkYwL1xvgr9c9y'
accesstokensecret = 'uOwbZGLE3WyevrWkKPaJu9rjtSY5IZJ3TE7pVJU8tp9ud'
consumerkey = '2lWIAi4Z6UKKBxv33YTtpqilM'
consumersecret = 'm7uNftueKNzg8LTG6s8WHDkMGII3DBXoXbbySnjzS0dHS6oTll'

authorization = OAuthHandler(consumerkey, consumersecret)
authorization.set_access_token(accesstoken, accesstokensecret)

cons = get_hate_terms('./data/conservative.csv')
ind = get_hate_terms('./data/independent.csv')
labour = get_hate_terms('./data/labour.csv')
lib_dem = get_hate_terms('./data/lib_dem.csv')

terms = cons + ind + labour + lib_dem

print(len(terms), terms)
time_limit = 15 * 60
jfile = open('./data/ua3.json', 'a')

api = tweepy.API(authorization, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_delay=5)
for i in terms:
    try:
        c = tweepy.Cursor(api.search, q=i, count=100, lang="en",
                          since="2019-12-9",
                          until="2019-12-17").items()
        print(i)
        start_time = time.time()
        for tweet in c:
            json.dump(tweet._json, jfile)
            jfile.write("%s" % '\n')
        if (time.time() - start_time) < time.time() + time_limit:
            # print('------------sleeping for 10 seconds------------------')
            print('reached limit')
            time.sleep(3)

    except Exception as e:
        print(e)
        print(e.__doc__)

    # In[ ]:

# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:




