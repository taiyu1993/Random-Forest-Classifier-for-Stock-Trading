## Taiyu Guo 
## GTID: 903256162, username: tguo40
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#import BestPossibleStrategy as bps
#import ManualStrategy as ms
import sys
sys.path.append('../')
from util import get_data, plot_data

def smaIndicator(sym="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),n=50):
    dates = pd.date_range(sd,ed)
    df = get_data([sym],dates)
    price = pd.DataFrame(data=df.iloc[:,1])
    price.insert(loc=1,column='SMA (50 days)',value=np.zeros(len(price.index)))
    price.iloc[:,1]=np.NAN
    price.insert(loc=2,column='SMA-IN (50 days)',value=np.zeros(len(price.index)))
    price.iloc[:,2]=np.NAN

    price.iloc[:,0] = price.iloc[:,0]/price.iloc[0,0]
    price.iloc[:,1] = price.iloc[:,0].rolling(window=n,center=False).mean()
    for i in range(n,len(price.index)):
        price.iloc[i,2]= price.iloc[i,0]/price.iloc[i-n:i,0].mean()-1

    price.iloc[:,0] = price.iloc[:,0]

    return price

def BollingerBand(sym='JPM',sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),n=50):
    dates = pd.date_range(sd,ed)
    df = get_data([sym],dates)
    price = pd.DataFrame(data=df.iloc[:,1])
    price.insert(loc=1,column='SMA (50 days)',value=np.zeros(len(price.index)))
    price.iloc[:,1]=np.NAN
    price.insert(loc=2,column='BB (Upper)',value=np.zeros(len(price.index)))
    price.iloc[:,2]=np.NAN
    price.insert(loc=3,column='BB (Lower)',value=np.zeros(len(price.index)))
    price.iloc[:,3]=np.NAN
    price.insert(loc=4,column='BB-IN',value=np.zeros(len(price.index)))
    price.iloc[:,4]=np.NAN

    price.iloc[:,0] = price.iloc[:,0]/price.iloc[0,0]
    sma = price.iloc[:,0].rolling(window=n,center=False).mean()
    std = price.iloc[:,0].rolling(window=n,center=False).std()
    price.iloc[:,1] = sma
    price.iloc[:,2] = sma+2*std
    price.iloc[:,3] = sma-2*std
    price.iloc[:,4] = (price.iloc[:,0] - price.iloc[:,1])/(2*std);

    return price

def MACD(sym='JPM',sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),n=50):
    dates = pd.date_range(sd,ed)
    df = get_data([sym],dates)
    price = pd.DataFrame(data=df.iloc[:,1])
    price.insert(loc=1,column='EWMA (12 days)',value=np.zeros(len(price.index)))
    price.iloc[:,1]=np.NAN
    price.insert(loc=2,column='EWMA (26 days)',value=np.zeros(len(price.index)))
    price.iloc[:,2]=np.NAN
    price.insert(loc=3,column='MACD Line',value=np.zeros(len(price.index)))
    price.iloc[:,3]=np.NAN
    price.insert(loc=4,column='MACD Signal',value=np.zeros(len(price.index)))
    price.iloc[:,4]=np.NAN

    price.iloc[:,0] = price.iloc[:,0]/price.iloc[0,0]

    a1 = 2.0/13.0
    a2 = 2.0/27.0
    mean12 = price.iloc[0:12,0].mean()
    mean26 = price.iloc[0:26,0].mean()

    for i in range(12,len(price.index)):
        if(i==12):
            price.iloc[i,1] = mean12
        else:
            price.iloc[i,1] = a1*price.iloc[i,0]+(1-a1)*price.iloc[i-1,1]


    for i in range(26,len(price.index)):
        if(i==26):
            price.iloc[i,2] = mean26
        else:
            price.iloc[i,2] = a2*price.iloc[i,0]+(1-a2)*price.iloc[i-1,2]

    # MACD Line
    price.iloc[:,3] = price.iloc[:,1]-price.iloc[:,2]

    a3 = 2.0/10.0
    mean9 = price.iloc[26:35,3].mean()

    for i in range(35,len(price.index)):
        if(i==35):
            price.iloc[i,4] = mean9
        else:
            price.iloc[i,4] = a3*price.iloc[i,3]+(1-a3)*price.iloc[i-1,4]

    return price

def main():
    sym = 'JPM'
    #sd = dt.datetime(2008,1,1)
    #ed = dt.datetime(2009,12,31)
    sd = dt.datetime(2010,1,1)
    ed = dt.datetime(2011,12,31)

    #n=50
    #price = BollingerBand(sym,sd,ed,n)
    #price = MACD(sym,sd,ed,n)
    #price = smaIndicator(sym,sd,ed,n)
    #plot_data(price.iloc[:,0:4])
    #plot_data(price)

    # graph = price.ix[:,3:5].plot(color=['blue','green'],linewidth=0.8)
    # # #graph = price[['BB-IN']].plot(color='blue',linewidth=0.8)
    # graph.set_xlabel('Date')
    # graph.set_ylabel('Indicator value')
    # plt.grid(linestyle='dotted')
    # plt.title("MACD Indicator")
    # fmt = mdates.DateFormatter("%b %Y")
    # graph.xaxis.set_major_formatter(fmt)
    # plt.show()

    #st = bps.BestPossibleStrategy()
    st = ms.ManualStrategy()
    trades_df= st.testPolicy(symbol="JPM",sd=sd,ed=ed,sv=100000)
    #print(trades_df)

if __name__ == "__main__": main()
