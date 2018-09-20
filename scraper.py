from bs4 import BeautifulSoup
import urllib3
import sqlite3 as sql3
import os
from hashlib import md5

http = urllib3.PoolManager()
request = http.request('GET', 'https://eskoly.sk/hlavna113/jedalen')
if request.status == 200:

    raw_data = request.data
    soup = BeautifulSoup(raw_data, "html.parser")

    original_hash=md5(str(soup.findAll("tr")).encode('utf-8')).hexdigest()
    print("html:", original_hash)

    if not os.path.isfile("data.sqlite"):
        open("data.sqlite", "w").close()

    connection = sql3.connect("data.sqlite")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS main(date TEXT, menu TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS versions(hash TEXT)")
    connection.commit()

    hash=cursor.execute("SELECT * FROM versions").fetchone()
    if hash:hash=hash[0]
    print("data:",hash)

    if not hash == original_hash:
        print("Data difference found")

        res = []
        for i in soup.findAll("tr")[2:-1]:
            i = repr(i).replace("<br/>", "\n")
            i = BeautifulSoup(i, "html.parser")
            for j in i.findAll("td")[0:2]:
                if not j.text.split("\n") == ['']:
                    res.append(j.text.split("\n"))

        for i in range(1, len(res), 2):
            res[i] = res[i][0:-1]

        for i in range(0, len(res), 2):
            date = str(res[i][1]).replace(". ", "-")
            meals = str(res[i + 1])
            date_in_db = cursor.execute("SELECT date FROM main WHERE date=(?)", (date,)).fetchall()
            meal_in_db = cursor.execute("SELECT menu FROM main WHERE menu=(?)", (meals,)).fetchall()
            if date_in_db and meal_in_db:
                print("Data for date", date, "are up to date")
            else:
                cursor.execute("INSERT INTO main VALUES(?,?)", (date, meals))
                connection.commit()
                print("Data for date", date, "were updated")

        cursor.execute("INSERT INTO versions VALUES(?)",
                       (md5(str(soup.findAll("tr")).encode('utf-8')).hexdigest(),))
        connection.commit()

    else:
        print("Data are up to date")
