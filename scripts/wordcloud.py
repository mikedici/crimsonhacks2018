#!/usr/bin/python3
import json
import MySQLdb as Database
from warnings import filterwarnings
from time import sleep

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
    data = list(myconnections.query("SELECT hashtag, raw_text FROM tweet"))
    myconnections.close()

    crypto = {"Bitcoin": [], "Etherium": [], "Litecoin": [], "Zcash": []}

    for i in range(len(data)):
        temp = []
        temp.append(data[i][1])

        temp = temp[0].replace("\\n", " ")
        temp = temp.replace("\n", " ")
        temp = temp.replace("=", " ")
        temp = temp.replace("\n\n", " ")
        temp = temp.replace(",", "")
        temp = temp.replace("RT", "")
        temp = temp.replace("…", "")
        temp = temp.replace("\\\\", "")
        temp = temp.replace(":", "")
        temp = temp.replace("//", "")
        temp = temp.replace("/", "")
        temp = temp.replace("'", "")
        temp = temp.replace('"', "")
        if data[i][0] == "#btc" or data[i][0] == "#bitcoin":
            crypto["Bitcoin"].extend(temp.split(" "))
        elif data[i][0] == "#zcash" or data[i][0] == "#zec":
            crypto["Zcash"].extend(temp.split(" "))
        elif data[i][0] == "#etherium":
            crypto["Etherium"].extend(temp.split(" "))
        elif data[i][0] == "#litecoin":
            crypto["Litecoin"].extend(temp.split(" "))
        else:
            pass;
    print(crypto)

    for key in crypto.keys():

        with open(str(key) + ".js", "w") as o:
            temp_string = "var " + str(key) + "= ["
            for word in range(len(crypto[key])):
                temp_string += "{text: '" + str(crypto[key][word]) + "' ,"

                temp_count = 0
                for wordcount in crypto[key]:
                    if wordcount == crypto[key][word]:
                        temp_count += 1
                temp_string += "size: " + str(temp_count % 30) + "}"
                if word < len(crypto[key]) - 1:
                    temp_string += ", "
                else:
                    temp_string += "];"
            o.write(temp_string)
            # o.write("var " + str(key) + "= ")
            # o.write(json.dumps(crypto[key], ensure_ascii=False))


if __name__ == "__main__":
    # while True:
    print("got this far")
    main()
    print("waiting")
    # sleep(30 * 60)
