import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import json
credentials = None
with open("creds.json", "r") as f:
    global credentials
    credentials = json.load(f)

class TwitterClient:

    def __init__(self, creds):
        self.consumer_key = creds["consumer_key"]
        self.consumer_secret = creds["consumer_secret"]
        self.access_token = creds["access_token"]
        self.access_token_secret = creds["access_token_secret"]
        self.auth = None
        self.api = None
        try:
            self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
            self.auth.set_access_token(self.access_token, self.access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)", " ", tweet).split())

    def get_tweet_sentiment(tweet):
        analysis = TextBlob(clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        tweets = []

        try:
            print(self.api)
            fetched_tweets = self.api.search(q=query, count=count, tweet_mode="extended")

            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.full_text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text)

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))


def main():
    thing = TwitterClient(credentials)
    tweets = thing.get_tweets(query='Donald Trump', count=200)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    print("Neutral tweets percentage: {} % \ ".format(100 * (len(tweets) - len(ntweets) - len(ptweets) )/ len(tweets)))

    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

        print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])


if __name__ == "__main__":
    main()
