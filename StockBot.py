#import alpca_trade_api as tradeapi
import time
from yahoo_fin import stock_info as si

def trade():
    counter=0;
    while True:
        counter+=1
        amzn=si.get_live_price("amzn")
        print(counter)
        print(amzn);
        time.sleep(60)

trade()
