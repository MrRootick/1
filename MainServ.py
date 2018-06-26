import os
import wex
import sqlite3
import bitfinex
import exmo
import comparison
import yobit
import telebot
import tokenTelegram
import random
import time
from flask import Flask, request

TOKEN = tokenTelegram.key
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
CHANNEL_NAME = '-1001275366258'
########################################################################################################################
#                                   цикл                                                                               #
########################################################################################################################

def timed_job():
     coin = ['btc_usd','btc_rur','btc_eur',
             'ltc_btc','ltc_usd','ltc_rur','ltc_eur',
             'dsh_btc','dsh_usd','dsh_rur','dsh_eur','dsh_ltc','dsh_eth','dsh_zec',
             'eth_btc','eth_usd','eth_eur','eth_ltc','eth_rur','eth_zec',
             'bch_usd','bch_btc','bch_rur','bch_eur','bch_ltc','bch_eth','bch_dsh','bch_zec',
             'zec_btc','zec_usd','zec_ltc']
     i = 0
     while i <len(coin):
         wex.Api(coin[i])
         i=i+1
     from datetime import datetime
     now = str(datetime.now())
     print('#####'+now+'#####'+'\n'+'Синхронизация Wex.nz с бд, успешно')

     coin = ['BTC_USD', 'BTC_RUB', 'BTC_EUR',
             'LTC_BTC', 'LTC_USD', 'LTC_RUB',
             'LTC_EUR', 'DASH_BTC', 'DASH_USD',
             'DASH_RUB', 'ETH_BTC', 'ETH_USD',
             'ETH_EUR', 'ETH_LTC', 'ETH_RUB',
             'BCH_USD', 'BCH_BTC', 'BCH_RUB',
             'BCH_ETH', 'ZEC_BTC', 'ZEC_USD']
     a = 0
     while a <len(coin):
         exmo.Api(coin[a])
         a = a + 1
     from datetime import datetime
     now = str(datetime.now())
     print('#####' + now + '#####' + '\n' + 'Синхронизация Exmo.com с бд, успешно')
     """
     coin = ['btcusd', 'btceur',
             'ethusd', 'ethbtc',
             'dshusd', 'dshbtc',
             'bchusd', 'bchbtc', 'bcheth',
             'ltcusd', 'ltcbtc',
             'zecbtc', 'zecusd']
     i = 0
     while i <len(coin):
         bitfinex.Api(coin[i])
         i = i + 1
     from datetime import datetime
     now = str(datetime.now())
     print('#####' + now + '#####' + '\n' + 'Синхронизация bitfinex.com с бд, успешно')
    """
     coin = ['btc_usd', 'btc_rur',
             'ltc_btc', 'ltc_usd', 'ltc_rur',
             'dash_btc', 'dash_usd', 'dash_rur', 'dash_eth',
             'eth_btc', 'eth_usd', 'eth_rur',
             'bcc_usd', 'bcc_btc', 'bcc_rur', 'bcc_eth',
             'zec_btc', 'zec_usd']
     i = 0
     while i < len(coin):

         i = i + 1
     print('#####' + now + '#####' + '\n' + 'Синхронизация yobit.net с бд, успешно')

########################################################################################################################
#                                   Логи                                                                               #
########################################################################################################################
def log(message,answer):
    print("/n ------")
    from datetime import datetime
    now=datetime.now()
    print(now)
    print("Message from  {0} {1}. (id = {2}) \n Text = {3}".format(message.from_user.first_name, message.from_user.last_name,
                                                                   str(message.from_user.id), message.text))
    answer = str(answer)
    print("Bot answered : ", answer)

    f = open('log.txt', 'a')
    from datetime import datetime
    now = str(datetime.now())
    f.write("--------------------------" + now+"--------------------------"+'\n' + "Message from {0} {1}. (id = {2}) \n Text = {3}"
            .format(message.from_user.first_name,message.from_user.last_name,
                    str(message.from_user.id),message.text)
            +'\n'+"Bot answered : "
            +'\n' + answer+'\n'+'\n')
    f.close()


    id = "{0}".format(str(message.from_user.id))
    first_name = "{0}".format(message.from_user.first_name)
    last_name = "{0}".format(message.from_user.last_name)

    add_user(id, first_name, last_name)


def add_user(id, first_name, last_name):            #запимсь в БД
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO Users (id,first_name,last_name) VALUES (?, ?, ?)",(id,first_name,last_name))
        print("New User")
        conn.commit()
        c.close()
        conn.close()
    except sqlite3.IntegrityError:
        print()


########################################################################################################################
#                                   Команды для бота                                                                   #
########################################################################################################################

@bot.message_handler(commands=['start'])  # Обработка команды start
def handle_text(message):

    answer = "Чо каво сучара"
    log(message, answer)
    bot.send_message(message.chat.id, answer )




def new_post_key():
    try:
        conn = sqlite3.connect('key.db')
        c = conn.cursor()
        q=random.randint(1,47000)
        c.execute("SELECT asd FROM qqq WHERE id='{}'".format(q))
        value = c.fetchone()
        key = str(value[0])
        if key != None:
            bot.send_message(CHANNEL_NAME, key)
            c.close()
            conn.close()
            time.sleep(60*10)
            new_post_key()


        else:
            time.sleep(10)
            c.close()
            conn.close()
            print("Пусто")
            new_post_key()

    except:
        print('Какая то ошибка')
        new_post_key()

@bot.message_handler(commands=['startkey'])  # Обработка команды start
def handle_text(message):
    answer = "Ключи раздаются"
    bot.send_message(message.chat.id, answer )
    new_post_key()



@bot.message_handler(commands=['analys'])  # Обработка команды start
def handle_text(message):
    f = open('temp', 'w')
    answer=" Жди около минуты пока обновятся данные"
    log(message, answer)
    bot.send_message(message.chat.id, answer)
    timed_job()
    brige = ['Wex', 'exmo',  'Yobit'] # 'fenix', добавить когда будет больше 10к бачей
    for y in range(0, 3):
        for i in range(0, 3):
            for x in range(0, 26):
                answer=comparison.analys(brige,y,i,x)
                if answer!=None:
                    f.write(answer+'\n'+'\n')
    f.close()
    f=open('temp','r')
    answ= f.read()
    log(message, answ)
    bot.send_message(message.chat.id, answ)
    f.close()

@bot.message_handler(commands=['wex'])  # Обработка команды Wex
def handle_text(message):
    f = open('temp_wex', 'w')
    from datetime import datetime
    now = str(datetime.now())
    coin = ['btc_usd','btc_rur','btc_eur',
            'ltc_btc','ltc_usd','ltc_rur','ltc_eur',
            'dsh_btc','dsh_usd','dsh_rur','dsh_eur','dsh_ltc','dsh_eth','dsh_zec',
            'eth_btc','eth_usd','eth_eur','eth_ltc','eth_rur','eth_zec',
            'bch_usd','bch_btc','bch_rur','bch_eur','bch_ltc','bch_eth','bch_dsh','bch_zec',
            'zec_btc','zec_usd','zec_ltc']
    i = 0
    while i <len(coin):
        answer = ('####' + now + '####' +
                  '\n' + wex.Api(coin[i])+'\n'+'\n')
        f.write(answer)
        i=i+1
    f.close()
    f=open('temp','r')
    answ= f.read()
    log(message, answ)
    bot.send_message(message.chat.id, answ)
    f.close()


@bot.message_handler(commands=['yobit'])  # Обработка команды Wex
def handle_text(message):
    f = open('temp', 'w')
    from datetime import datetime
    now = str(datetime.now())
    coin = ['btc_usd', 'btc_rur',
            'ltc_btc', 'ltc_usd', 'ltc_rur',
            'dash_btc', 'dash_usd', 'dash_rur', 'dash_eth',
            'eth_btc', 'eth_usd', 'eth_rur',
            'bcc_usd', 'bcc_btc', 'bcc_rur', 'bcc_eth',
            'zec_btc', 'zec_usd']
    i = 0
    while i < len(coin):
        answer = ('####' + now + '####' +
                  '\n' + yobit.Api(coin[i]) + '\n' + '\n')
        print(answer)
        i = i + 1
    f.close()
    f = open('temp', 'r')
    answ = f.read()
    log(message, answ)
    bot.send_message(message.chat.id, answ)
    f.close()


@bot.message_handler(commands=['exmo'])  # Обработка команды Wex
def handle_text(message):
    f = open('temp_exmo', 'w')
    from datetime import datetime
    now = str(datetime.now())
    coin = ['BTC_USD','BTC_RUB','BTC_EUR',
            'LTC_BTC','LTC_USD','LTC_RUB',
            'LTC_EUR','DASH_BTC','DASH_USD',
            'DASH_RUB','ETH_BTC','ETH_USD',
            'ETH_EUR','ETH_LTC','ETH_RUB',
            'BCH_USD','BCH_BTC','BCH_RUB',
            'BCH_ETH','ZEC_BTC','ZEC_USD']
    i = 0
    while i <len(coin):
        answer = ('####' + now + '####' +
                  '\n' + exmo.Api(coin[i])+'\n'+'\n')
        f.write(answer)
        i = i + 1
    f.close()
    f = open('temp_exmo', 'r')
    answ = f.read()
    log(message, answ)
    bot.send_message(message.chat.id, answ)
    f.close()


@bot.message_handler(commands=['bitfenix'])  # Обработка команды Wex
def handle_text(message):
    f = open('temp_bitfenix', 'w')
    from datetime import datetime
    now = str(datetime.now())
    coin = ['btcusd','btceur',
            'ethusd','ethbtc',
            'dshusd','dshbtc',
            'bchusd','bchbtc','bcheth',
            'ltcusd','ltcbtc',
            'zecbtc','zecusd']
    i = 0
    while i <len(coin):
        answer = ('####' + now + '####' +
                  '\n' + bitfinex.Api(coin[i])+'\n'+'\n')
        f.write(answer)
        i = i + 1
    f.close()
    f = open('temp_bitfenix', 'r')
    answ = f.read()
    log(message, answ)
    bot.send_message(message.chat.id, answ)
    f.close()


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://botbtc.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))