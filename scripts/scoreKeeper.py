import re
import MySQLdb
import datetime
from datetime import timedelta
import json

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Tweet:
    # This is the class that will handle tweets

    @staticmethod
    def analyze_sentiment(raw_text):
        analyzer = SentimentIntensityAnalyzer()
        return analyzer.polarity_scores(raw_text)

    @staticmethod
    def strip_mentions(raw_text):
        # use a regular expression to collect @mentions
        ment_list = []
        ment_pat = re.compile(r'@[a-zA-Z0-9$%&*]+')
        ment_list.extend(re.findall(ment_pat, raw_text))
        return ment_list

    @staticmethod
    def strip_tags(raw_text):
        # use a regular expression to collect the hashtags from the tweet
        tags_list = []
        tag_pat = re.compile(r'#[a-zA-Z0-9_$%&*]+')
        tags_list.extend(re.findall(tag_pat, raw_text))
        return tags_list

    def __init__(self, tweetID, tweetDate, raw_text):
        self._raw = raw_text
        self._id = tweetID
        self._date = tweetDate

        if self._raw[0:2] == "RT":
            self.isRt = True
        else:
            self.isRt = False

        self._tags = []
        # hashtags

        self._mentions = []
        # @ mentions

        self._wfreq = []
        # word frequencies
        self._stripped = self.strip_tweet()

        self._sentiment = self.analyze_sentiment(self.get_stripped())
        # generate sentiment scores

    def get_id(self):
        return self._id

    def get_date(self):
        return self._date

    def get_stripped(self):
        return self._stripped

    def get_raw(self):
        return self._raw

    def get_tags(self):
        return self._tags

    def get_wfreq(self):
        return self._wfreq

    def get_mentions(self):
        return self._mentions

    def get_sentiment(self):
        return self._sentiment

    def set_tags(self, tags_list):
        self._tags = tags_list

    def set_mentions(self, ment_list):
        self._mentions = ment_list

    def set_sentiment(self, sentiment):
        self._sentiment = sentiment

    def strip_t_and_m(self):
        # call both the strip static methods
        temp = self.get_raw()
        self.set_tags(self.strip_tags(temp))
        self.set_mentions(self.strip_mentions(temp))

    def strip_tweet(self):
        self.strip_t_and_m()
        temp = str(self.get_raw())
        for i in self.get_tags():
            temp = temp.replace(i, "")
        for j in self.get_mentions():
            temp = temp.replace(j, "")
        return temp


def main():
    scores = []
    querys = ["SELECT tweet_id, tweet_date, raw_text FROM twitter.tweet WHERE hashtag = '#ethereum'",
              "SELECT tweet_id, tweet_date, raw_text FROM twitter.tweet WHERE hashtag = '#litecoin'",
              "SELECT tweet_id, tweet_date, raw_text FROM twitter.tweet WHERE hashtag = '#bitcoin'",
              "SELECT tweet_id, tweet_date, raw_text FROM twitter.tweet WHERE hashtag = '#zcash'",
              "SELECT tweet_id, tweet_date, raw_text FROM twitter.tweet WHERE hashtag = '#hodl'",
              "SELECT tweet_id, tweet_date, raw_text FROM twitter.tweet WHERE hashtag = '#btc'",
              "SELECT tweet_id, tweet_date, raw_text FROM twitter.tweet WHERE hashtag = '#crypto'",
              "SELECT tweet_id, tweet_date, raw_text FROM twitter.tweet WHERE hashtag = '#zec'"]

    db = MySQLdb.connect(host="crimsonhacks2018.csqidy9gdlbh.us-west-2.rds.amazonaws.com", port=3306, user='crimsonapp',
                         db='twitter', charset='utf8', autocommit='on')
    cursor = db.cursor()
    for k in querys:
        print(k)
        cursor.execute(k)

        rawtweets = []
        rawtweets.extend(cursor.fetchall())

        processed = []
        temp = rawtweets.pop()

        for i in range(len(rawtweets)):
            temp = rawtweets.pop()
            processed.append(Tweet(temp[0], temp[1], temp[2]))
        sum = 0
        for j in processed:

            day_mult = 7 - int((datetime.datetime.now() - j.get_date()).days)
            if day_mult < 0:
                continue
            normalized = float(j.get_sentiment()['compound']) * day_mult
            if normalized <= -0.05:
                normalized *= 5
            sum += normalized
        scores.append(sum)


    combined_scores = {"ethereum": scores[0], "litecoin": scores[1], 'bitcoin': ((scores[2] + scores[5])/2.0), 'zcash': (scores[3] + scores[-1])/2.0, "hodl" : scores[4], "crypto":scores[-2]}

    with open("scores.json", "w") as o:
        o.write(json.dumps(combined_scores))

    print(combined_scores)

    # cursor.execute(
    #     "INSERT INTO `twitter`.`aggregateSentiment` (`ethereum`, `litecoin`, `bitcoin`, `zcash`, `hodl`, `btc`," +
    #     " `crypto`, `zec`) VALUES(" + str(scores[0]) + ", " + str(scores[1]) + ", " + str(scores[2]) + ", "
    #     + str(scores[3]) + ", " + str(scores[4]) + ", " + str(scores[5]) + ", " + str(scores[6]) + ", "
    #     + str(scores[7]) + ")")


if __name__ == '__main__':
    main()
