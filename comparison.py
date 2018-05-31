import sqlite3

def comparison (brige, y, i, x):
    try:
        coin = ['BTC_USD', 'BTC_RUB', 'BTC_EUR',
                'LTC_BTC', 'LTC_USD', 'LTC_RUB', 'LTC_EUR',
                'DSH_BTC', 'DSH_USD', 'DSH_RUB', 'DSH_EUR', 'DSH_LTC', 'DSH_ETH', 'DSH_ZEC',
                'ETH_BTC', 'ETH_USD', 'ETH_EUR', 'ETH_LTC', 'ETH_RUB', 'ETH_ZEC',
                'BCH_USD', 'BCH_BTC', 'BCH_RUB', 'BCH_EUR', 'BCH_LTC', 'BCH_ETH', 'BCH_DSH', 'BCH_ZEC',
                'ZEC_BTC', 'ZEC_USD', 'ZEC_LTC']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        cn = coin[x]

        br = brige[y]
        c.execute("SELECT Buy, Sell FROM {0} WHERE Coin='{1}'".format(br, cn))
        value = c.fetchone()
        buy = str(value[0])

        br = brige[i]
        c.execute("SELECT Buy, Sell FROM {0} WHERE Coin='{1}'".format(br, cn))
        value = c.fetchone()
        c.close()
        conn.close()
        sell = str(value[1])
        course = [cn, buy, sell]
        return (course)

    except TypeError:
        return

def analys(brige,y,i,x):
        if brige[y]!=brige[i]:
            try:
                abc=comparison(brige, y, i, x)
                buy=float(abc[1])
                sell=float(abc[2])
                proc = (sell-buy) /(buy*0.01)
                if buy!=None or sell!=None:
                    if proc >= 5:
                        if buy < sell and (buy*0.01)<(sell-buy):

                            return (abc[0] + '\n' +
                                    'Buy ' + abc[1] + ' ' + brige[y] + '\n' +
                                    'Sell ' + abc[2] + ' ' + brige[i] + '\n'
                                    +'profit ' + str(proc)[0:4]+'%')
            except TypeError:
                return
