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


from datetime import datetime
now = str(datetime.now())
coin = ['btc_usd','btc_rur','btc_eur',
        'ltc_btc','ltc_usd','ltc_rur','ltc_eur',
        'dsh_btc','dsh_usd','dsh_rur','dsh_eur','dsh_ltc','dsh_eth','dsh_zec',
        'eth_btc','eth_usd','eth_eur','eth_ltc','eth_rur','eth_zec',
        'bch_usd','bch_btc','bch_rur','bch_eur','bch_ltc','bch_eth','bch_dsh','bch_zec',
        'zec_btc','zec_usd','zec_ltc']
i = 0
while i <= 30:
    answer = ('####' + now + '####' +
              '\n' + Api(coin[i])+'\n'+'\n')
    print(answer)
    i=i+1
