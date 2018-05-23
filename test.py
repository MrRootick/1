import urllib
import requests
import bs4
import json
########################################################################################################################
#                                   Выгрузка данных с биржи yobit.net                                                     #
########################################################################################################################

def Api():


    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    htm = urllib.request.urlopen('https://yobit.net/api/2/btc_usd/ticker').read()
    htm = requests.get(headers=headers)
    soup = bs4.BeautifulSoup(htm, "html.parser")
    txt = str(soup)
    data = json.loads(txt)
    buy=data[coin]['buy']
    sell=(data[coin]['sell'])
    buy=str(buy)
    sell=str(sell)
    return ("Yobit " + " buy " + buy + '\n' + " sell " + sell)
print (Api())
