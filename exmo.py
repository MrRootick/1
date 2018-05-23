import urllib
import bs4
import sqlite3
import json
########################################################################################################################
#                                   Выгрузка данных с биржи exmo.com                                                   #
########################################################################################################################

def Api(coin):

    htm = urllib.request.urlopen('https://api.exmo.com/v1/order_book/?pair='+coin).read()
    soup = bs4.BeautifulSoup(htm, "html.parser")
    txt = str(soup)
    data = json.loads(txt)
    buy=data[coin]['ask_top']
    sell=(data[coin]['bid_top'])
    buy=str(buy)
    sell=str(sell)
    if coin[0:4] == 'DASH':
        coin='DSH'+coin[4:8]

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO exmo (Coin,Buy,Sell) VALUES (?, ?, ?)", (coin, buy, sell))
        conn.commit()
        c.close()
        conn.close()
    except sqlite3.IntegrityError:
        print("error sql")
    return ("exmo " + coin + '\n' + " buy " + buy + '\n' + " sell " + sell)
