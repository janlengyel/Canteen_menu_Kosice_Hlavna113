from bs4 import BeautifulSoup
import urllib3
import sqlite3 as sql3
import os

http = urllib3.PoolManager()
request = http.request('GET', 'https://eskoly.sk/hlavna113/jedalen')
if request.status==200:
    raw_data = request.data
    soup = BeautifulSoup(raw_data, "html.parser")

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
# print(soup_yeyyy.findAll("tr")[2:-1])

# A really big TODO
