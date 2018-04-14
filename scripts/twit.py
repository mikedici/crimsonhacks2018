import tweepy
import json

credentials = None

with open("creds.json", "r") as f:
    json.loads(f)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

print('Hello World')
