import tokenTelegram
import wex
import sqlite3
import bitfinex
import exmo
import comparison
import yobit

import os

import telebot
from flask import Flask, request
# -*- coding: utf-8 -*-
bot = telebot.TeleBot(tokenTelegram.key)
bott = tokenTelegram.key
bott = str(bott)

server = Flask(__name__)


########################################################################################################################
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
########################################################################################################################

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
     while i <= 27:
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
     while a <= 20:
         exmo.Api(coin[a])
         a = a + 1
     from datetime import datetime
     now = str(datetime.now())
     print('#####' + now + '#####' + '\n' + 'Синхронизация Exmo.com с бд, успешно')

     coin = ['btcusd', 'btceur',
             'ethusd', 'ethbtc',
             'dshusd', 'dshbtc',
             'bchusd', 'bchbtc', 'bcheth',
             'ltcusd', 'ltcbtc',
             'zecbtc', 'zecusd']
     i = 0
     while i <= 12:
         bitfinex.Api(coin[i])
         i = i + 1
     from datetime import datetime
     now = str(datetime.now())
     print('#####' + now + '#####' + '\n' + 'Синхронизация bitfinex.com с бд, успешно')










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

@bot.message_handler(commands=['analys'])  # Обработка команды start
def handle_text(message):
    f = open('temp', 'w')
    answer=" Жди около минуты пока обновятся данные"
    log(message, answer)
    bot.send_message(message.chat.id, answer)
    timed_job()
    brige = ['Wex', 'exmo', 'fenix']
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
    open('wex', 'w').close()
    f = open('temp', 'w')
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
    coin = ['btc_usd','btc_rur','btc_eur',
            'ltc_btc','ltc_usd','ltc_rur','ltc_eur',
            'dsh_btc','dsh_usd','dsh_rur','dsh_eur','dsh_ltc','dsh_eth','dsh_zec',
            'eth_btc','eth_usd','eth_eur','eth_ltc','eth_rur','eth_zec',
            'bch_usd','bch_btc','bch_rur','bch_eur','bch_ltc','bch_eth','bch_dsh','bch_zec',
            'zec_btc','zec_usd','zec_ltc']
    i = 0
    while i <= 27:
        answer = ('####' + now + '####' +
                  '\n' + yobit.Api(coin[i])+'\n'+'\n')
        f.write(answer)
        i = i + 1
    f.close()
    f = open('temp', 'r')
    answ = f.read()
    log(message, answ)
    bot.send_message(message.chat.id, answ)
    f.close()


@bot.message_handler(commands=['exmo'])  # Обработка команды Wex
def handle_text(message):
    f = open('temp', 'w')
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
    while i <= 20:
        answer = ('####' + now + '####' +
                  '\n' + exmo.Api(coin[i])+'\n'+'\n')
        f.write(answer)
        i = i + 1
    f.close()
    f = open('temp', 'r')
    answ = f.read()
    log(message, answ)
    bot.send_message(message.chat.id, answ)
    f.close()


@bot.message_handler(commands=['bitfenix'])  # Обработка команды Wex
def handle_text(message):
    f = open('temp', 'w')
    from datetime import datetime
    now = str(datetime.now())
    coin = ['btcusd','btceur',
            'ethusd','ethbtc',
            'dshusd','dshbtc',
            'bchusd','bchbtc','bcheth',
            'ltcusd','ltcbtc',
            'zecbtc','zecusd']
    i = 0
    while i <= 12:
        answer = ('####' + now + '####' +
                  '\n' + bitfinex.Api(coin[i])+'\n'+'\n')
        f.write(answer)
        i = i + 1
    f.close()
    f = open('temp', 'r')
    answ = f.read()
    log(message, answ)
    bot.send_message(message.chat.id, answ)
    f.close()


@server.route('/' + bott, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://botbtc.herokuapp.com/' + bott)
    return "!", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)