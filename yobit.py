import urllib
import bs4
import sqlite3
import json
########################################################################################################################
#                                   Выгрузка данных с биржи yobit.net                                                     #
########################################################################################################################

def Api(coin):

    htm = urllib.request.urlopen('http://yobit.net/api/2/'+coin+'/ticker').read()
    soup = bs4.BeautifulSoup(htm, "html.parser")
    txt = str(soup)
    data = json.loads(txt)
    buy=data[coin]['buy']
    sell=(data[coin]['sell'])
    buy=str(buy)
    sell=str(sell)
    coin = str(coin.upper())
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO yobit (Coin,Buy,Sell) VALUES (?, ?, ?)", (coin, buy, sell))
        conn.commit()
        c.close()
        conn.close()
    except sqlite3.IntegrityError:
        print("error sql")
    return ("Yobit " + coin + '\n' + " buy " + buy + '\n' + " sell " + sell)
