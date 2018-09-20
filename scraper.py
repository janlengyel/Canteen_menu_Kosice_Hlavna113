from bs4 import BeautifulSoup
import urllib3
import sqlite3 as sql3
import os
from hashlib import md5

http = urllib3.PoolManager()
request = http.request('GET', 'https://eskoly.sk/hlavna113/jedalen')
if request.status==200:

    if not os.path.isfile("hash.txt"):
        open("hash.txt", "w").close()

    with open("hash.txt","r") as text:
        text=text.read()
        if text:
            hash=text
            print("file:",hash)

    raw_data = request.data
    soup = BeautifulSoup(raw_data, "html.parser")

    print("html:",md5(str(soup.findAll("tr")).encode('utf-8')).hexdigest())
    
    if not hash==md5(str(soup.findAll("tr")).encode('utf-8')).hexdigest():

        res = []
        for i in soup.findAll("tr")[2:-1]:
            i = repr(i).replace("<br/>", "\n")
            i = BeautifulSoup(i, "html.parser")
            for j in i.findAll("td")[0:2]:
                if not j.text.split("\n") == ['']:
                    res.append(j.text.split("\n"))

        for i in range(1, len(res), 2):
            res[i] = res[i][0:-1]
        for i in res:
            print(i)

        if os.path.exists("data.sqlite"):
            os.remove("data.sqlite")
        if not os.path.isfile("data.sqlite"):
            open("data.sqlite", "w").close()
        connection=sql3.connect("data.sqlite")
        cursor=connection.cursor()
        for i in range(int(len(res)/2)):
            cursor.execute("CREATE TABLE day"+str(i)+" (menu TEXT)")
            connection.commit()
            for j in res[i*2+1]:
                cursor.execute("INSERT INTO day" + str(i) + " values(?)", (j,))
                connection.commit()

        with open("hash.txt", "w") as text:
            text.write(md5(str(soup.findAll("tr")).encode('utf-8')).hexdigest())

    else:
        print("Data are up to date")

# print(soup_yeyyy.findAll("tr")[2:-1])

# A really big TODO
