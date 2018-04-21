import requests
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("choice")
args = parser.parse_args()
sentiment = None
mychoice =""
if args.choice == "b":
    mychoice = "Bitcoin"
elif args.choice == "l":
    mychoice = "Litecoin"
elif args.choice == "z":
    mychoice = "Zcash"
elif args.choice == "e":
    mychoice = "Etherium"
else:
    print("b  bitcoin")
    print("l  litecoin")
    print("z  zcash")
    print("e  etherium")


req = requests.get("http://www.whatthehackshouldidowithmycrypto.com:8080")
values = req.json()
if values[mychoice] > 0:
    sentiment = "Positive"
elif values[mychoice] == 0:
    sentiment = "Neutral"
else:
    sentiment = "Negative"
os.system("sudo google_speech 'The outlook for " + str(mychoice) + " is " + str(sentiment) + "'")

