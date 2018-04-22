import json

total = 28231
freqs = {"#zcash": 1075, "#hodl": 4348, "#crypto": 4345,
         "#ethereum": 517, "#litecoin": 4923, "#bitcoin": 3152, "#btc": 6220, "#zec": 3651}

freqs["total"] = 28231

with open("frequency.json", "w") as o:
    o.write(json.dumps(freqs))