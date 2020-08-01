#importing files
import logging
from alice_blue import *
import pandas as pd
from datetime import datetime


#login credentials

logging.basicConfig(level=logging.DEBUG)
access_token = 'DLtnUQ2Kt1KfKcUAR0m-CIXpJZDyhqu0uNUAQI4UTHw.NbL4yhdClMnJYcueEXMcGq3D70bVP-w5AZOKFtjgWZg'
alice = AliceBlue(username='AB086867', password='chicu@24428', access_token=access_token,
                  master_contracts_to_download=['NSE', 'BSE', 'NFO'])

# Reading CSV for symbols
instrument_symbol = []
instruments = pd.read_csv('filename.csv', names=['tradingsymbol', 'instrument_token'])
for symbol in instruments['tradingsymbol']:
    instrument_symbol.append(alice.get_instrument_by_symbol('NSE', '{}'.format(symbol)))


socket_opened = False
a = []
dict = {}
b = 0


def event_handler_quote_update(message):
    print(f"quote update {message}")
    ts = int(message['exchange_time_stamp'])
    c = datetime.utcfromtimestamp(ts).strftime('%H:%M')
    d = int(datetime.utcfromtimestamp(ts).strftime('%H'))
    e = int(datetime.utcfromtimestamp(ts).strftime('%M'))
    print(c)
    global b
    global a
    if (d==9 and m==15):
        if (b < len(instrument_symbol)):
            a.append(message['ltp'])
            b=b+1
        else:
            b = 0
    elif (d == 9 and e > 15 and e <=30):
        cd = message['symbol']
        global dict
        dict[cd].append[message['ltp']]


def open_callback():
    global socket_opened
    socket_opened = True


alice.start_websocket(subscribe_callback=event_handler_quote_update,
                      socket_open_callback=open_callback,
                      run_in_background=True)
while (socket_opened == False):
    pass

alice.subscribe(instrument_symbol[1:], LiveFeedType.MARKET_DATA)

alice.get_all_subscriptions()
now = datetime.now()
hrs = int(now.strftime("%H"))
min=int(now.strftime("%m"))



#SELL BUY telling at 9:31
if(hrs==9 and min==31):
    alice.unsubscribe(instrument_symbol[1:], LiveFeedType.MARKET_DATA)
index=0
buy=0
sell=0
for symbol in instruments:
    buy=0
    sell=0
    try:
        for j in dict[symbol].values:
            if(a[index]>j):
              buy=buy+1
            elif(a[index]<j):
                sell=sell+1
        if(buy==15):
            print("buy",symbol)
        elif(sell==15):
            print("sell",symbol)
        else:
            print("nothing",symbol)
    except:
        print("symbol data not found",symbol)
