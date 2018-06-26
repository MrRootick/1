import urllib.request
import bs4
import sqlite3
import json
########################################################################################################################
#                                   Выгрузка данных с биржи yobit.net                                                     #
########################################################################################################################

def Api(coin):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"
    req = urllib.request.Request('http://yobit.net/api/2/'+coin+'/ticker',  headers = headers)
    htm = urllib.request.urlopen(req).read()
    soup = bs4.BeautifulSoup(htm, "html.parser")
    txt = str(soup)
    data = json.loads(txt)
    buy=data['ticker']['buy']
    sell=(data['ticker']['sell'])
    buy=str(buy)
    sell=str(sell)
    coin = str(coin.upper())
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO Yobit (Coin,Buy,Sell) VALUES (?, ?, ?)", (coin, buy, sell))
        conn.commit()
        c.close()
        conn.close()
    except sqlite3.IntegrityError:
        print("error sql")
    return ("Yobit " + coin + '\n' + " buy " + buy + '\n' + " sell " + sell)


