import tweepy
import json


def get_tweets(creds, username):
    # Authorization to consumer key and consumer secret
    auth = tweepy.OAuthHandler(creds["consumer_key"], creds["consumer_secret"])

    # Access to user's access key and access secret
    auth.set_access_token(creds["access_token"], creds["access_token_secret"])

    # Calling API
    api = tweepy.API(auth)

    # 200 tweets to be extracted
    number_of_tweets=200
    tweets = api.user_timeline(screen_name=username)

    # empty list
    tmp = []
    for tweet in tweets:
        tmp.append(tweet.text)
    print(tmp)


def main():

    twitacct = "realDonaldTrump"
    credentials = None
    with open("creds.json", "r") as f:
        credentials = json.load(f)

    get_tweets(credentials, twitacct)


if __name__ == "__main__":
    main()

