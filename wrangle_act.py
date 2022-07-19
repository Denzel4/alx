#!/usr/bin/env python
# coding: utf-8

# # Project: Wrangling and Analyze Data

#imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import seaborn as sns
import tweepy
import json
x = {"sec_key":"sjscbZ8MqpCy9FcSPhOXDgoVg","secret":"gdEQxtOSTaBkIQdj1SlRDwM9iAvBdZFZqgGzndAkBMd0H08pTr",
"token":"AAAAAAAAAAAAAAAAAAAAAAhTeAEAAAAA23c0LL54qgRDuNM6VaY64RIqBa4%3DA17AWAxSM3qV8zjGwLq32MLFt6IqHhh61mrSO0bLoV3bGuq1Dz"}

archive = pd.read_csv('twitter-archive-enhanced.csv')

cred = json.dumps(x)

with open('twits_cred.json','w') as outfile:
    outfile.write(cred)
    
cred = pd.read_json('twits_cred.json',lines=True)

cred.keys()

cred.sec_key.values[0]


#passing credentials
consumer_key = cred.sec_key.values[0]
consumer_secret = cred.secret.values[0]

consumer_secret

auth = tweepy.OAuth2BearerHandler(cred.token.values[0])
api = tweepy.API(auth,wait_on_rate_limit=True)

archive.keys()

archive.tweet_id[1].dtype

tweet_id = archive.tweet_id

tweet = api.get_status(tweet_id[20])
print(tweet.retweet_count)
print(tweet.favorite_count)

np.sum(tweet_id.isna())

new_data = pd.DataFrame()

new_data['tweet_id'] = archive.tweet_id

new_data.head()

tweet_id[19]


len(tweet_id)

def twit_count(tweet_id):
    rtweet = []
    for sid in list(tweet_id):
        try:
                tweet=api.get_status(sid,tweet_mode='extended')
                retweets= (sid,tweet.retweet_count)
                rtweet.append(retweets)
        except tweepy.NotFound as e:
            if getattr(e, 'api_code', None) == 404:
                print(e)
                continue
        except tweepy.Forbidden as f:
            if getattr(f,'api_code',None)==403:
                print(f.reason)
                break
        except StopIteration:
            break
    print('Successfuly fetched all retweets')
    return  dict(rtweet)

def loc_count(tweet_id):
    loc= []
    for sid in list(tweet_id):
        try:
                tweet=api.get_status(sid,tweet_mode='extended')
                location= (sid,tweet.geo)
                loc.append(location)
        except tweepy.NotFound as e:
            if getattr(e, 'api_code', None) == 404:
                print(e)
                continue
        except tweepy.Forbidden as f:
            if getattr(f,'api_code',None)==403:
                print(f.reason)
                break
        except StopIteration:
            break
    print('Successfuly fetched all location')
    return  dict(loc)

def fav_count(tweet_id):
    fav= []
    for sid in list(tweet_id):
        try:
                tweet=api.get_status(sid,tweet_mode='extended')
                fv= (sid,tweet.favorite_count)
                fav.append(fv)
        except tweepy.NotFound as e:
            if getattr(e, 'api_code', None) == 404:
                print(e)
                continue
        except tweepy.Forbidden as f:
            if getattr(f,'api_code',None)==403:
                print(f.reason)
                break
        except StopIteration:
            break
    print('Successfuly fetched all likes')
    return  dict(fav)

retweet = twit_count(tweet_id)

location = loc_count(tweet_id)

fav = fav_count(tweet_id)


df = pd.DataFrame(list(fav.items()), columns = ['tweet_id','likes'])
df.to_csv('likes.csv')

df1 = pd.DataFrame(list(location.items()), columns = ['tweet_id','location'])
df1.to_csv('location.csv')

df2 = pd.DataFrame(list(fav.items()), columns = ['tweet_id','retweets'])
df2.to_csv('retweet_.csv') 