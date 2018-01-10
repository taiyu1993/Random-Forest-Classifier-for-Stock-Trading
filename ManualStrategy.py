## Taiyu Guo
## GTID: 903256162, username: tguo40
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from util import get_data, plot_data
from marketsimcode import compute_portvals
from indicators import BollingerBand, smaIndicator, MACD

class ManualStrategy(object):

  def __init__(self):
      pass

  def testPolicy(self,symbol="JPM",sd=dt.datetime(2010,1,1),ed=dt.datetime(2011,12,31),sv=100000):
      n = 50
      price = BollingerBand(symbol,sd,ed,n)
      ind1 = price.iloc[:,4]
      price = smaIndicator(symbol,sd,ed,n)
      ind2 = price.iloc[:,2]
      price = MACD(symbol,sd,ed,n)
      ind3 = price.iloc[:,3]

      #benchmark
      benchmark = pd.DataFrame(index=[sd],columns=['Symbol','Order','Shares'])
      benchmark.iloc[0,:]=[symbol,'BUY',1000]
      portBM = compute_portvals(order=benchmark, start_date=sd, end_date=ed, start_val=sv, commission=9.95, impact=0.005)
      #Strategy
      noDays = len(price.index)
      order = pd.DataFrame(index=price.index,columns=['Symbol','Order','Shares'])
      hold =  0

      for i in range(n-1,noDays):
          if hold==0 and (ind1.iloc[i]>0.5 or ind2.iloc[i]>0.03 or ind3.iloc[i]>0.05):
              order.iloc[i] = [symbol, 'BUY', 1000]
              hold = 1000
          elif hold==0 and (ind1.iloc[i]<-0.5 or ind2.iloc[i]<-0.03 or ind3.iloc[i]<-0.05):
              order.iloc[i] = [symbol, 'SELL', 1000]
              hold = -1000
          elif hold==-1000 and (ind1.iloc[i]>0.5 or ind2.iloc[i]>0.03 or ind3.iloc[i]>0.05):
              order.iloc[i-1] = [symbol,'BUY',2000]
              hold = 1000
          elif hold==1000 and (ind1.iloc[i]<-0.5 or ind2.iloc[i]<-0.03 or ind3.iloc[i]<-0.05):
              order.iloc[i-1] = [symbol,'SELL',2000]
              hold = -1000

      order = order.dropna(axis=0,how='any')
      portManual = compute_portvals(order=order,start_date=sd,end_date=ed,start_val=sv,commission=0,impact=0)

      return portBM, portManual
