#!/usr/bin/python3
import tweepy
import json
import re
import MySQLdb as Database
from warnings import filterwarnings
from textblob import TextBlob
from time import sleep

filterwarnings('ignore', category=Database.Warning)

interesting = ["#hodl", "#btc", "#crypto", "#litecoin", "#ethereum", "#bitcoin", "#zcash", "#zec"]


class Daemon:
    """ Daemon is the class that abstracts connecting to the database  to create a new Daemon you must pass it the path
        to a json file containing all the information to connect to the server"""

    def __init__(self, path, verbosity=False):
        self.verbose_output = verbosity
        if self.verbose_output:
            print("Initializing Daemon")
        self.dbinfo = self._set_auth(path, self.verbose_output)

        self._db_connection = Database.connect(host=self.dbinfo['host'], port=int(self.dbinfo['port']),
                                               user=self.dbinfo['user'], passwd=self.dbinfo['passwd'],
                                               db=self.dbinfo['db'], charset="utf8")
        self._cursor = self._db_connection.cursor()

    def get_db(self):
        if self.verbose_output:
            print("DB Name: " + str(self.dbinfo['db']))
        return self.dbinfo['db']

    def commit(self):
        if self.verbose_output:
            print("Commiting Changes")
        self._db_connection.commit()
        return "success"

    def close(self):
        self._db_connection.close()

    def query(self, sql):
        if self.verbose_output:
            print("Executing query: " + str(sql))
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    @staticmethod
    def _set_auth(filepath, verbosity=False):
        if verbosity:
            print("Getting DB info from: " + str(filepath))
        with open(filepath, "r") as f:
            return json.load(f)


def get_hashtag_tweets(creds, hashtag):
    # Authorization to consumer key and consumer secret
    auth = tweepy.OAuthHandler(creds["consumer_key"], creds["consumer_secret"])

    # Access to user's access key and access secret
    auth.set_access_token(creds["access_token"], creds["access_token_secret"])

    # Calling API
    api = tweepy.API(auth)
    tweets = api.search(q=hashtag, rpp=100, tweet_mode='extended')
    tmp = []
    for tweet in tweets:
        tmp.append(tweet)
    return tmp


def get_user_tweets(creds, username):
    # Authorization to consumer key and consumer secret
    auth = tweepy.OAuthHandler(creds["consumer_key"], creds["consumer_secret"])

    # Access to user's access key and access secret
    auth.set_access_token(creds["access_token"], creds["access_token_secret"])

    # Calling API
    api = tweepy.API(auth)

    # 200 tweets to be extracted
    tweets = api.user_timeline(screen_name=username, count=200, tweet_mode='extended')

    # empty list
    tmp = []
    for tweet in tweets:
        tmp.append(tweet)
    return tmp


def create_insert(tweet_list):
    outstring = ""
    for item in range(len(tweet_list)):
        outstring += str(tweet_list[item])
        if item < len(tweet_list) - 1:
            outstring += ", "
    return outstring


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


def main():
    myconnections = Daemon("db.json")

    credentials = None
    with open("creds.json", "r") as f:
        credentials = json.load(f)

    # tweet_data = get_user_tweets(credentials, "sudointell")
    # values = []

    values = []
    for i in interesting:
        tweet_data = get_hashtag_tweets(credentials, i)
        for j in tweet_data:
            for tweet in tweet_data:
                try:
                    poly = tweet.place.bounding_box.coordinates[0]
                    lats = []
                    longs = []
                    outlat = 0
                    outlong = 0
                    for point in range(len(poly)):
                        lats.append(poly[point][0])
                        longs.append(poly[point][1])

                    for z in lats:
                        outlat += z
                    for y in longs:
                        outlong += y

                    outlong = outlong / len(longs)
                    outlat = outlat / len(lats)


                except AttributeError:
                    outlat = ""
                    outlong = ""
            values.append((j.id_str, i, outlat, outlong, get_tweet_sentiment(j.full_text), j.full_text,
                           j.created_at.strftime('%Y-%m-%d-%H-%M-%S')))

    myconnections.query(
        "INSERT ignore INTO tweet (tweet_id, hashtag, lat, longitude, sentiment, raw_text, tweet_date) values" + str(
            create_insert(values)))
    myconnections.commit()
    myconnections.close()


if __name__ == "__main__":
    while True:
        try:
            print("got this far")
            main()
            print("waiting")
            sleep(15 * 60)
        except tweepy.RateLimitError:
            print("not so fast")
            sleep(2 * 60)
