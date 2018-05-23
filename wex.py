import urllib
import bs4
import sqlite3
import json
########################################################################################################################
#                                   Выгрузка данных с биржи WEX.nz                                                     #
########################################################################################################################

def Api(coin):

    htm = urllib.request.urlopen('https://wex.nz/api/3/ticker/'+coin).read()
    soup = bs4.BeautifulSoup(htm, "html.parser")
    txt = str(soup)
    data = json.loads(txt)
    buy=data[coin]['buy']
    sell=(data[coin]['sell'])
    buy=str(buy)
    sell=str(sell)
    coin = str(coin.upper())
    if coin[4:7]== 'RUR':                   # для общего стандарта отображения валют в БД
        coin=coin[0:4]+"RUB"
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO Wex (Coin,Buy,Sell) VALUES (?, ?, ?)", (coin, buy, sell))
        conn.commit()
        c.close()
        conn.close()
    except sqlite3.IntegrityError:
        print("error sql")
    return ("wex " + coin + '\n' + " buy " + buy + '\n' + " sell " + sell)
