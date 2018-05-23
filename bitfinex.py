import urllib
import bs4
import sqlite3
import json
########################################################################################################################
#                                   Выгрузка данных с биржи bitfinex.com                                               #
########################################################################################################################

def Api(coin):
    try:
        htm = urllib.request.urlopen('https://api.bitfinex.com/v1/pubticker/'+coin).read()
        soup = bs4.BeautifulSoup(htm, "html.parser")
        txt = str(soup)
        data = json.loads(txt)

        buy=data['ask']
        sell=data['bid']
        buy=str(buy)
        sell=str(sell)
        coin = str(coin.upper())
        coin_1 = coin[0:3:1]
        coin_2 = coin[3:7:1]
        coin=(coin_1+"_"+coin_2)                            # для общего стандарта отображения валют в БД
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO fenix (Coin,Buy,Sell) VALUES (?, ?, ?)", (coin, buy, sell))
            conn.commit()
            c.close()
            conn.close()
        except sqlite3.IntegrityError:
            print("error sql")
        return ("bitfenix " + coin_1 + "_" + coin_2 + '\n' + " buy " + buy + '\n' + " sell " + sell)
    except urllib.error.HTTPError:
        print ("Error, limit!!!")
        return ("Error, limit!!!")