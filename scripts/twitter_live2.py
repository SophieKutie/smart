#!/usr/bin/env python
# coding: utf-8

# In[1]:
# from django.conf.project_template.manage import main
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API as api
from tweepy import Cursor
import tweepy
import time
import json
import pandas as pd
import matplotlib.pyplot as plt
import re
import os, sys
import pprint
import matplotlib.pyplot as plt
import math
import random
import csv

# In[2]:


'''
get a list of hateful terms. These ae collected from hatebase.org using the hatespeech-vocabulary-collection script
stored in hatespeech-terms.csv file
csv_file_name should include the full path to the file
the file should be formatted as one column labelled 'term' and as many terms as required

term
term 1
term 2
term 3
...
'''


def get_hate_terms(csv_file_name):
    terms = pd.read_csv(csv_file_name, encoding='utf')  ### option for manual input
    # terms.sort_values('term', inplace=True)
    # print('Before removing duplicated terms: ', terms.count())
    terms.drop_duplicates(keep='first', inplace=True)
    # print('After removing duplicated terms: ',  terms.count())
    return terms['terms'].astype(str).values.tolist()


# read the terms from a folder
# the terms_files directory should include one or more csv files with terms in them
terms_file = os.listdir('./test/data/user_handles/')
print('term files ', terms_file)
terms = []
for i in terms_file:
    terms += get_hate_terms('./test/data/user_handles/' + i)

print(terms)

# In[3]:


'''
Twitter only accepts n number of terms at a time
Use this function if we have a large number of terms so we supply twitter with small list of terms in each API call
return randomised list of terms
'''


def get_list_of_list(list_of_terms, sublist_size):
    random_list = random.sample(list_of_terms, len(list_of_terms))
    for i in range(0, len(random_list), sublist_size):
        # Create an index range for l of n items:
        yield random_list[i:i + sublist_size]


term_list = list(get_list_of_list(terms, 10))
print('Number of lists of terms to process: %d' % len(term_list))
for t in term_list:
    print('Start time on the following list %s of length %d' % (time.strftime("%Y-%m-%d, %H:%M:%S"), len(t)))
    print(t)

print('Finished time %s' % time.strftime("%Y-%m-%d, %H:%M:%S"))

# In[4]:


accesstoken = '1192071683483557888-JsajbXeIZV4yO7heVLBiyKoLmcwE2D'
accesstokensecret = 'iHopL1lf1l7vYQw13sbtNpumfRyjJ3JOoPXMwtadj8uSm'
consumerkey = '4nmllrY1s4k2x8ClNEMA4Ohvd'
consumersecret = 'GBmKtYX2wrGVDxbGn2kPbYbuD4wUGEq2i6RVI1dzT8jCmgGxYX'

authorization = OAuthHandler(consumerkey, consumersecret)
authorization.set_access_token(accesstoken, accesstokensecret)


class MyStreamListener(StreamListener):

    def __init__(self, output_file):
        self.output_file = output_file
        self.siesta = 0
        self.nightnight = 0
        self.start_time = time.time()
        self.time_limit = time_limit
        self.tweet_file = open(self.output_file, 'a')

        super(MyStreamListener, self).__init__()

    def on_status(self, status):
        if (time.time() - self.start_time) < self.time_limit:
            try:
                if 'extended_tweet' in status._json:
                    json.dump(status._json, self.tweet_file)
                    self.tweet_file.write("%s" % '\n')
            except  Exception as e:
                print('failed on writing data to file:', e)
                pass
            return True
        else:
            self.tweet_file.close()
            return False

    def on_error(self, status_code):
        print('Error:', str(status_code))
        if status_code == 420:
            sleepy = 60 * math.pow(2, self.siesta)
            print(time.strftime("%Y%m%d_%H%M%S"))
            print("A reconnection attempt will occur in " + str(sleepy / 60) + " minutes.")
            print('''
            *******************************************************************
            From Twitter Streaming API Documentation
            420: Rate Limited
            The client has connected too frequently. For example, an
            endpoint returns this status if:
            - A client makes too many login attempts in a short period
              of time.
            - Too many copies of an application attempt to authenticate
              with the same credentials.
            *******************************************************************
            ''')
            time.sleep(sleepy)
            self.siesta += 1
        else:
            sleepy = 5 * math.pow(2, self.nightnight)
            print(time.strftime("%Y%m%d_%H%M%S"))
            print('A reconnection attempt will occur in ', str(sleepy), ' seconds.')
            time.sleep(sleepy)
            self.nightnight += 1
        return True

    def on_limit(self, track):
        sleepy = 5 * math.pow(2, self.nightnight)
        print(time.strftime("%Y%m%d_%H%M%S"))
        print('A reconnection attempt will occur in ', str(sleepy), ' seconds.')
        time.sleep(sleepy)
        self.nightnight += 1
        sys.stderr.write("on_limit  " + track + "\n")
        return True

    def on_timeout(self):
        sleepy = 5 * math.pow(2, self.nightnight)
        print(time.strftime("%Y%m%d_%H%M%S"))
        print('Timeout ', str(sleepy), ' seconds.')
        time.sleep(sleepy)
        self.nightnight += 1
        return True

    # In[ ]:


# time_limit = 15 * 60
time_limit = 360  # in seconds


def run_script(start_date1, end_date1, output_file='./test/data/{datetime.now().strftime("%Y%m%d-%H%M%S")}_tweets.json',
               reps=1000):
    if start_date1 != 0 and end_date1 != 0:
        start_date1 = time.strptime(start_date1, "%Y-%m-%d")
        end_date1 = time.strptime(end_date1, "%Y-%m-%d")

    # #
    # # terms = get_hate_terms(terms)
    # term_list = list(get_list_of_list(terms, 10))
    # time_limit = 360  # in seconds

    # the following goes through the list of terms, which is a list of list
    # each sublist takes about 6 minutes, you can change the time limit for each list by resetting the time_limit variable value
    # we feed all the sublists (the full terms in the csv file) in onr hous
    for i in range(1, reps):
        print('Number of lists of terms to process: %d\n' % len(term_list))
        print(i, ' out of  1000  repition.\n')
        k = 0
        for terms in term_list:
            k += 1
            print('\t', k, ' out of  ', len(term_list), '  sets of terms.\n')
            print('Start time on the following list %s\n' % time.strftime("%Y-%m-%d, %H:%M:%S"))
            print(terms, '\n')
            start_time = time.time()

            try:
                twitterStream = Stream(authorization, MyStreamListener(output_file, time_limit))
                twitterStream.filter(track=terms, languages=["en"], stall_warnings=True)
                if (time.time() - start_time) < time.time() + time_limit:
                    # print('------------sleeping for 3 seconds------------------')
                    time.sleep(3)
                else:
                    if end_date1 > start_date1:
                        # stop
                        break
            except Exception as e:
                print(e)
                print(e.__doc__)

                # time.sleep(905)
            print('Finished round: %d at time %s' % (i, time.strftime("%Y-%m-%d, %H:%M:%S")))


from datetime import datetime

#
# output_file = f'./test/data/{datetime.now().strftime("%Y%m%d-%H%M%S")}_tweets.json'
# run_script(term_list, output_file=output_file, reps=5)

# if __name__ == "__main__":
#
#     main()

# In[ ]:


# In[ ]:
