#!/usr/bin/python3
import json
import MySQLdb as Database
from warnings import filterwarnings
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


def main():
    myconnections = Daemon("db.json")
    credentials = None

    with open("creds.json", "r") as f:
        credentials = json.load(f)
    data = myconnections.query("SELECT hashtag, sentiment FROM tweet")
    myconnections.close()

    crypto = {"Bitcoin": 0, "Etherium": 0, "Litecoin": 0, "Zcash": 0}

    for i in data:
        print(i)
        if i[0] == "#hodl" or i[0] == "#crypto":

            if i[1] == "positive" or i[1] == "neutral":
                crypto["Bitcoin"] += 0.25
                crypto["Etherium"] += 0.25
                crypto["Litecoin"] += 0.25
                crypto["Zcash"] += 0.25
            elif i[1] == "negative":
                crypto["Bitcoin"] -= 0.25
                crypto["Etherium"] -= 0.25
                crypto["Litecoin"] -= 0.25
                crypto["Zcash"] -= 0.25
            else:
                pass

        elif i[0] == "#btc" or i[0] == "#bitcoin":
            if i[1] == "positive" or i[1] == "neutral":
                crypto["Bitcoin"] += 1
            elif i[1] == "negative":
                crypto["Bitcoin"] -= 10
            else:
                pass

        elif i[0] == "zcash" or i[0] == "#zec":
            if i[1] == "positive" or i[1] == "neutral":
                crypto["Zcash"] += 1
            elif i[1] == "negative":
                crypto["Zcash"] -= 10
            else:
                pass

        elif i[0] == "#etherium":
            if i[1] == "positive" or i[1] == "neutral":
                crypto["Etherium"] += 1
            elif i[1] == "negative":
                crypto["Etherium"] -= 10
            else:
                pass

        elif i[0] == "#litecoin":
            if i[1] == "positive" or i[1] == "neutral":
                crypto["Litecoin"] += 1
            elif i[1] == "negative":
                crypto["Litecoin"] -= 10
            else:
                pass

    with open("/home/ubuntu/crimproj/wallet.json", "w") as o:
        o.write(json.dumps(crypto))


if __name__ == "__main__":

    while True:
        print("got this far")
        main()
        print("waiting")
        sleep(30 * 60)
