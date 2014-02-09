#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__license__ = "GPL"
__version__ = "0.0.5"
__maintainer__ = "s_0rtega"
__status__ = "Development"

import tweepy
import argparse
import PIL
import urllib
import os
from pprint import pprint

import watermark 

def crawlIt():
    parser = argparse.ArgumentParser(description='Tweepy Crawler a search. Download the tweets, save the images and add a watermark!')
    parser.add_argument('-t','--tags', help='Add tags for search and retreive tweets in CSV format', required=True)
    parser.add_argument('-w','--watermark', help='Put a watermark on each downloaded image', required=False, action='store_true')
    args = parser.parse_args()

    tags=args.tags.split(',')

    # == OAuth Authentication ==
    #
    # This mode of authentication is the new preferred way
    # of authenticating with Twitter.

    # The consumer keys can be found on your application's Details
    # page located at https://dev.twitter.com/apps (under "OAuth settings")
    consumer_key=""
    consumer_secret=""

    # The access tokens can be found on your applications's Details
    # page located at https://dev.twitter.com/apps (located 
    # under "Your access token")
    access_token=""
    access_token_secret=""

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # If the authentication was successful, you should
    # see the name of the account print out
    counters={}

    for tag in tags:
        count=0
        file=open(tag+"_tweetsT.txt","w")
        
        if not os.path.exists("Twitter_"+tag):
            os.makedirs("./Twitter_"+tag)
        
        for tweet in tweepy.Cursor(api.search,
                               q=tag,
                               count=100000,
                               include_entities=True).items():
            
            try:
                file.write(str(tweet.created_at)+"-"+tweet.text.encode('UTF-8')+"\n")
                image=tweet.entities['media'][0]['media_url']+":large"
                urllib.urlretrieve(image, "Twitter_"+tag+"/"+image.split("/")[-1].split(":")[0])

                if args.watermark:
                    watermark.putWatermark("Twitter_"+tag+"/"+image.split("/")[-1].split(":")[0], "@"+tweet.user.screen_name)
                    
            except Exception,e: 
                #print str(e)
                pass
                
            count+=1
        counters[tag]=count

    print "\nTotal downloaded tweets:\n"
    pprint(counters)

if __name__ == '__main__':
    crawlIt()
