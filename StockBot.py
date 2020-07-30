import alpaca_trade_api as tradeapi
import time
import pytz
import random
import datetime
import pkg_resources.py2_warn
import requests
import sys
from yahoo_fin import stock_info as si
positions=[0,0,0,0]
hold=[20, 20, 20, 20]
buyPrice=[0,0,0,0]
sellPrice=[0,0,0,0]
shares=[0,0,0,0]
print("Welcome to an Open Source Stock trading bot")
print("You will be updated periodically on your account equity, purchases and buying power")
#amzn=0 msft=1 goog=2 fb=3
apikey=input("Enter your Alpaca API Key: ")
secretkey=input("Enter your secret Key: ")
endpoint=input("Enter your endpoint: ")
api = tradeapi.REST(apikey, secretkey, endpoint, api_version='v2')
account=api.get_account()
end=False
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
                    if hold[0]>19:
                        analyze(amzn,amznl,0)
                    if hold[1]>19:
                        analyze(msft, msftl, 1)
                    if hold[2]>19:
                        analyze(goog, googl, 2)
                    if hold[3]>19:
                        analyze(fb,fbl,3)
                if end==True:
                    print("Market is now closed")
                    sys.exit(0)
                time.sleep(1)
                if counter%10==0:
                    account=api.get_account()
                    balance=float(account.equity)
                    power=float(account.cash)
                    print("The current time is: ")
                    current_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
                    print (current_time)
                    print("Current Cash on hand is is: $")
                    print(power)
                    print("Current Total Equity is: $")
                    print(balance)
                hold[0]+=1
                hold[1]+=1
                hold[2]+=1
                hold[3]+=1
            else:
                print("Market has Closed")
                break;
    else:
        print("Market is Currently Closed")


def analyze(symbol, hist, index):
    size=len(hist)
    names=""
    if index == 0:
        names="AMZN"
    elif index ==1:
        names="MSFT"
    elif index ==2:
        names="GOOG"
    elif index ==3:
        names="FB"
    currPrice=float(hist[size-1])
    account=api.get_account()
    balance=float(account.equity)
    if positions[index]!=0:
        difference=currPrice-buyPrice[index]
        percent= (difference/buyPrice[index])*100
        current_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
        if current_time.hour==15 and (current_time.minute>57):
            sell(names, positions[index], index)
            end=True
        elif hist[size-1]<hist[size-2] and hist[size-2]<hist[size-3]:
            sell(names, positions[index], index)
    elif positions[index]==0:
        current_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
        if current_time.hour==15 and (current_time.minute>57):
            end=True
        else:
            power=float(account.cash)
            if (float(hist[size-3])<float(hist[size-9]) and float(hist[size-1])>float(hist[size-2]) and float(hist[size-2])>float(hist[size-3]) and power>currPrice):
                maxShares=int(power/currPrice)
                if maxShares>0:
                    if maxShares==1:
                        purchaseNum=1
                    else:
                        purchaseNum=random.randrange(1,maxShares)
                    order(names,purchaseNum,index)


def order(name, number, index):
    print("Ordering....")
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
    numberstr=str(number);
    prices=str(buyPrice[index])
    print("Purchased "+name+" Number of Shares: "+numberstr+ " At $"+prices+ " Per Share")

def sell(name, number, index):
    api.submit_order(
        symbol=name,
        qty=number,
        side='sell',
        type='market',
        time_in_force='gtc'
    )
    strnum=str(number)
    pricesold=str(sellPrice[index])
    positions[index]-=number;
    if index==0:
        sellPrice[index]=si.get_live_price("amzn")
    elif index==1:
        sellPrice[index]=si.get_live_price("msft")
    elif index==2:
        sellPrice[index]=si.get_live_price("goog")
    elif index==3:
        sellPrice[index]=si.get_live_price("fb")
    print("Sold "+name+" Number of Shares: "+strnum+ " At $"+pricesold+ " Per Share")
    gain=(sellPrice[index]-buyPrice[index])
    gainstr=str(gain)
    if gain>=0:
        print("Sold at a gain of $"+gainstr+" Per Share")
    else:
        print("Sold at a loss of $"+gainstr+" Per Share")
        hold[index]=0

trade()
