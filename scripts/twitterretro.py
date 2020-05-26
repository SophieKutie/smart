#!/usr/bin/env python
# coding: utf-8

# In[2]:


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
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


terms = get_hate_terms('./test/data/user_handles/meghan.csv')
# cons = get_hate_terms('./test/data/abusive_terms.csv')
# ind = get_hate_terms('./test/data/abusive_terms.csv')
# labour = get_hate_terms('./test/data/abusive_terms.csv')
# lib_dem = get_hate_terms('test/data/abusive_terms.csv')

# terms = cons + ind + labour + lib_dem

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
terms = get_hate_terms('./test/data/user_handles/meghan.csv')
accesstoken = '1192071683483557888-JsajbXeIZV4yO7heVLBiyKoLmcwE2D'
accesstokensecret = 'iHopL1lf1l7vYQw13sbtNpumfRyjJ3JOoPXMwtadj8uSm'
consumerkey = '4nmllrY1s4k2x8ClNEMA4Ohvd'
consumersecret = 'GBmKtYX2wrGVDxbGn2kPbYbuD4wUGEq2i6RVI1dzT8jCmgGxYX'
authorization = OAuthHandler(consumerkey, consumersecret)
authorization.set_access_token(accesstoken, accesstokensecret)
api = tweepy.API(authorization, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_delay=5)
results = tweepy.Cursor(api.search, q=SEARCH_TERM, count=100, lang="en", since_id="2019-12-09",
                           until="2019-12-15")
for tweet in results.items():
    print(tweet)
# In[3]:




# cons = get_hate_terms('./data/conservative.csv')
# ind = get_hate_terms('./data/independent.csv')
# labour = get_hate_terms('./data/labour.csv')
# lib_dem = get_hate_terms('./data/lib_dem.csv')

terms = get_hate_terms('./test/data/user_handles/meghan.csv')

print(len(terms), terms)
time_limit = 15 * 60
jfile = open('./test/data/tweets.json', 'a')

def run_script(start_date1, end_date1, output_file='./test/data/{datetime.now().strftime("%Y%m%d-%H%M%S")}_tweets.json',
               reps=1000):
    if start_date1 != 0 and end_date1 != 0:
        start_date1 = time.strptime(start_date1, "%Y-%m-%d")
        end_date1 = time.strptime(end_date1, "%Y-%m-%d")

    for i in terms:
        try:
            c = tweepy.Cursor(api.search, q=i, count=100, lang="en",
                              since="2019-12-9",
                              until="2019-12-17").items()
            print(i)
            start_time = time.time()
            if c.num_tweets < 1:
                print(f"Cursor returned no tweets for '{i}' search")
            for tweet in c:
                json.dump(tweet._json, jfile)
                jfile.write("%s" % '\n')
            if (time.time() - start_time) < time.time() + time_limit:
                # print('------------sleeping for 10 seconds------------------')
                print(f'Reached limit{time_limit}waiting for twitter response')
                time.sleep(3)

        except Exception as e:
            print(e)
            print(e.__doc__)



#time limitnot working, reached limit message persists



# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


def main():
    # read the terms from a folder
    # the terms_files directory should include one or more csv files with terms in them
    terms_file = os.listdir('./test/data/user_handles/')  # '../media')  #ask Sardar for second location function
    print('term files', terms_file)
    terms = []
    for i in terms_file:
        terms += get_hate_terms("./test/data/user_handles/" + i)

    print(terms)

    #
    # terms = get_hate_terms(terms)
    term_list = list(get_list_of_list(terms, 10))
    time_limit = 360  # in seconds

    term_list = list(get_list_of_list(terms, 10))
    print('Number of lists of terms to process: %d' % len(term_list))
    for t in term_list:
        print('Start time on the following list %s of length %d' % (time.strftime("%Y-%m-%d, %H:%M:%S"), len(t)))
        print(t)

    print('Finished time %s' % time.strftime("%Y-%m-%d, %H:%M:%S"))

    from datetime import datetime
    output_file = f'./test/data/{datetime.now().strftime("%Y%m%d-%H%M%S")}_tweets.json'
    run_script(term_list, output_file=output_file, reps=5)


if __name__ == "__main__":
    # import sys
    #
    # folder, number_of_terms = sys.args
    main()



