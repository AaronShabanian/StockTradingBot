import alpaca_trade_api as tradeapi
import time
import pytz
import random
import datetime
import requests
from yahoo_fin import stock_info as si
positions=[0,0,0,0]
buyPrice=[0,0,0,0]
sellPrice=[0,0,0,0]
shares=[0,0,0,0]
print("Welcome to an Open Source Stock trading bot")
print("You will be updated periodically on your account equity, purchases and buying power")
#amzn=0 msft=1 goog=2 fb=3
api = tradeapi.REST('PKPBENNGKZ9E10NWEYLN', 'cAwATJ534258CdTvc7jJN0LlvqfPOh4PKdw3xz53', 'https://paper-api.alpaca.markets', api_version='v2')
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
            if clock.is_open:
                counter+=1
                print(counter)
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
                if counter>10:
                    analyze(amzn,amznl,0)
                    analyze(msft, msftl, 1)
                    analyze(goog, googl, 2)
                    analyze(fb,fbl,3)
                time.sleep(60)
                if counter%10==0:
                    account=api.get_account()
                    balance=float(account.equity)
                    power=account.buying_power
                    print("The current time is: ")
                    current_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
                    print (current_time)
                    print("Current Stock Buying Power is: $")
                    print(power)
                    print("Current Total Equity is: $")
                    print(balance)
            else:
                print("Market has Closed")
                break;
    else:
        print("Market is Currently Closed")


def analyze(symbol, hist, index):
    size=len(hist)
    currPrice=int(hist[size-1])
    account=api.get_account()
    balance=float(account.equity)
    if positions[index]!=0:
        difference=currPrice-buyPrice[index]
        percent= (difference/buyPrice[index])*100
        current_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
        if hist[size-1]<hist[size-2]:
            sell(symbol, positions[index], index)
        elif current_time.hour==3 and current_time.minute==58:
            sell(symbol, positions[index], index)
    elif positions[index]==0:
        power=int(account.buying_power)
        if int(hist[size-1])<int(hist[size-9]) and int(hist[size-1])>int(hist[size-2]) and power>currPrice:
            maxShares=int(power/currPrice)
            purchaseNum=random.randrange(1,maxShares)
            order(symbol,purchaseNum,index)


def order(name, number, index):
    api.submit_order(
        symbol=name,
        qty=number,
        side='buy',
        type='market',
        time_in_force='gtc'
    )
    positions[index]+=number;
    #Checking the price you purchsed at
    if index==0:
        buyPrice[index]=si.get_live_price("amzn")
    elif index==1:
        buyPrice[index]=si.get_live_price("msft")
    elif index==2:
        buyPrice[index]=si.get_live_price("goog")
    elif index==3:
        buyPrice[index]=si.get_live_price("fb")
    print("Purchased "+name+" Number of Shares: "+number+ " At $"+buyPrice[index]+ " Per Share")

def sell(name, number, index):
    api.submit_order(
        symbol=name,
        qty=number,
        side='sell',
        type='market',
        time_in_force='gtc'
    )
    positions[index]-=number;
    if index==0:
        sellPrice[index]=si.get_live_price("amzn")
    elif index==1:
        sellPrice[index]=si.get_live_price("msft")
    elif index==2:
        sellPrice[index]=si.get_live_price("goog")
    elif index==3:
        sellPrice[index]=si.get_live_price("fb")
    print("Sold "+name+" Number of Shares: "+number+ " At $"+sellPrice[index]+ " Per Share")
    gain=sellPrice[index]-buyPrice[index]
    if gain>=0:
        print("Sold at a gain of $"+gain+" Per Share")
    else:
        print("Sold at a loss of $"+gain+" Per Share")

trade()
