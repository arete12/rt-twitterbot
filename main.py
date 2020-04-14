import tweepy
import os
import sys

auth = tweepy.OAuthHandler("", "") # keys
auth.set_access_token("", "") # access tokens

api = tweepy.API(auth)

tweets = []
user = "" # user whose tweets will be retweeted
count = 5

f = open("date.txt", "r+")
date = f.read()

try:
    for tweet in api.user_timeline(id=user, count=count):
        tweets.append((tweet.created_at,tweet.id,tweet.text))
except BaseException as e:
    print("failed on_status,",str(e))

tweetdate = int(str(tweets[0][0]).replace(":","").replace("-","").replace(" ",""))

if tweetdate > int(date) and "RT @" not in tweets[0][2]:
    api.update_status("") # sentence to comment with

f.seek(0)
f.write(str(tweetdate))
f.close()
