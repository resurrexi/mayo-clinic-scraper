import requests
import re
import string
import sqlite3
import os
from bs4 import BeautifulSoup as bs

dbpath = r"C:\Users\resurrexi\Dropbox\databases"
letters = list(string.ascii_uppercase)

# Init sqlite connection
conn = sqlite3.connect(os.path.join(dbpath, 'mayo.db'))
cur = conn.cursor()


def val_check(tbl, col, val):
    cur.execute("SELECT * FROM {} WHERE {} = ?".format(tbl, col), (val,))
    if cur.fetchone():
        return True
    else:
        return False


# Create tables if they don't exist
cur.executescript("""
CREATE TABLE IF NOT EXISTS conditions (id INTEGER PRIMARY KEY,
                                       condition,
                                       link);
""")
conn.commit()

for letter in letters:
    r = requests.get('http://www.mayoclinic.org/diseases-conditions/index?letter={}'.format(letter)).text

    soup = bs(r, "html.parser")

    items = soup.find("div", id="index").find("ol").find_all("li")

    for item in items:
        item_ascii = re.sub(u"\u2018|\u2019", "'", item.text).replace(u"\u2014", "-")
        if not val_check("conditions", "condition", item_ascii):
            print("Inserting {}...".format(item_ascii))
            cur.execute("INSERT INTO conditions (condition, link) VALUES (?, ?)", (item_ascii, item.a['href'],))
            conn.commit()
