import alpaca_trade_api as tradeapi
import time
import requests
from yahoo_fin import stock_info as si
positions=[0,0,0,0]
#amzn=0 msft=1 goog=2 fb=3
api = tradeapi.REST('PKQJOI25DAFM21LXXIYE', 'NL4hFAkbVPXmFLIqhzddXcZ1jWemq4zSBoOkQjWW', 'https://paper-api.alpaca.markets', api_version='v2')
def trade():
    #anything with an L at the end is data that is stored every minute
    clock = api.get_clock()
    poftfolio=api.list_positions()
    if clock.is_open:
        amznl=[]
        msftl=[]
        fbl=[]
        googl=[]
        counter=0;
        while True:
            counter+=1
            #Getting live prices and storing them in an array to analyze
            amzn=si.get_live_price("amzn")
            msft=si.get_live_price("msft")
            goog=si.get_live_price("goog")
            fb=si.get_live_price("fb")
            amznl.append(amzn)
            msftl.append(msft)
            googl.append(goog)
            fbl.append(fb)
            if counter>10:
                amznl.pop(0)
                msftl.pop(0)
                googl.pop(0)
                fbl.pop(0)
            analyze(amzn,amznl,0)
            analyze(msft, msftl, 1)
            analyze(goog, googl, 2)
            analyze(fb,fbl,3)
            time.sleep(60)
    else:
        print("Market is Currently Closed")


def analyze(symbol, hist, index):
    account=api.get_account()
    balance=float(account.equity)
    print("analyze")
    if positions[index]!=0:
        sell(symbol, amount, index)
    elif positions[index]==0:
        print("Nothing owned")


def order(name, number, index):
    api.submit_order(
        symbol=name,
        qty=number,
        side='buy',
        type='market',
        time_in_force='gtc'
    )
    positions[index]+=number;


def sell(name, number, index):
    api.submit_order(
        symbol=name,
        qty=number,
        side='sell',
        type='market',
        time_in_force='gtc'
    )
    positions[index]-=number;
trade()
