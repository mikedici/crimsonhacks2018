import tweepy
import json
import MySQLdb as Database
from warnings import filterwarnings

filterwarnings('ignore', category=Database.Warning)

interesting = ["#hodl", "#btc", "#crypto", "#litecoin", "#etherium", "#bitcoin", "#zcash", "#zec"]


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
    number_of_tweets = 200
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


def main():
    myconnections = Daemon("db.json", True)
    print(myconnections.query("SELECT * FROM tweet"))

    
    credentials = None
    with open("creds.json", "r") as f:
        credentials = json.load(f)

    # tweet_data = get_user_tweets(credentials, "sudointell")
    values = []
    for i in interesting:
        tweet_data = get_hashtag_tweets(credentials, i)
        for j in tweet_data:
            values.append((i, "", "", "", j.full_text, j.created_at.strftime('%Y-%m-%d')))

    myconnections.query("INSERT INTO tweet (hashtag, lat, longitude, sentiment, raw_text, tweet_date) values" + str(create_insert(values)))
    myconnections.commit()


if __name__ == "__main__":
    main()
