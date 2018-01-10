"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
"""
## Taiyu Guo
## GTID: 903256162, username: tguo40

import datetime as dt
import pandas as pd
import random
import RTLearner as rt
import BagLearner as bl
import indicators as ind
import numpy as np
import sys
from marketsimcode import compute_portvals
sys.path.append("../")
import util as ut

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.learner = bl.BagLearner(learner = rt.RTLearner,kwargs = {"leaf_size":15}, bags = 30, boost = False, verbose = False)

    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):
        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later

        n = 5 # n-day returns
        N = 50 # n-day SMA, BB, MACD indicators
        noDays = prices.shape[0]

        # compute indicators
        smaInd = ind.smaIndicator(symbol,sd,ed,N)
        bbInd = ind.BollingerBand(symbol,sd,ed,N)
        macdInd = ind.MACD(symbol,sd,ed,N)

        temp = np.empty((prices.shape[0],1))
        temp[:] = np.nan
        ret = pd.DataFrame(index=prices.index,data=temp,columns=[symbol])
        for i in range(noDays-n):
            ret.iloc[i] = (prices.iloc[i+n]/(prices.iloc[i]*(1+self.impact))) - 1

        YBUY = 0.03+self.impact
        YSELL = -0.03-self.impact

        data = np.zeros((noDays-N-n,4))
        data[0:,0] = smaInd.iloc[N:noDays-n,2]
        data[0:,1] = bbInd.iloc[N:noDays-n,4]
        data[0:,2] = macdInd.iloc[N:noDays-n,4]

        for i in range(noDays-N-n):
            if ret.iloc[N+i,0]>=YBUY:
                data[i,3] = 1
            elif ret.iloc[N+i,0]<=YSELL:
                data[i,3] = -1
            else:
                data[i,3] = 0

        trainX = data[:,0:-1]
        trainY = data[:,-1]
        self.learner.addEvidence(trainX,trainY)

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later

        n = 5
        N = 50
        noDays = prices.shape[0]

        smaInd = ind.smaIndicator(symbol,sd,ed,N)
        bbInd = ind.BollingerBand(symbol,sd,ed,N)
        macdInd = ind.MACD(symbol,sd,ed,N)

        testX = np.zeros((noDays-N-n,3))
        testX[0:,0] = smaInd.iloc[N:noDays-n,2]
        testX[0:,1] = bbInd.iloc[N:noDays-n,4]
        testX[0:,2] = macdInd.iloc[N:noDays-n,4]

        res = self.learner.query(testX)

        days = prices.index[N:noDays-n]
        order = pd.DataFrame(index=days,columns=['Order'])
        hold = 0

        for i in range(noDays-N-n):
            if hold==0 and (res[i]>0):
                order.iloc[i] = 1000
                hold = 1000
            elif hold==0 and (res[i]<0):
                order.iloc[i]=-1000
                hold = -1000
            elif hold==-1000 and (res[i]>0):
                order.iloc[i] = 2000
                hold = 1000
            elif hold==1000 and (res[i]<0):
                order.iloc[i] = -2000
                hold = -1000
            else:
                order.iloc[i] = 0
        return order

    def test(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later

        n = 5
        N = 50
        noDays = prices.shape[0]

        smaInd = ind.smaIndicator(symbol,sd,ed,N)
        bbInd = ind.BollingerBand(symbol,sd,ed,N)
        macdInd = ind.MACD(symbol,sd,ed,N)

        testX = np.zeros((noDays-N-n,3))
        testX[0:,0] = smaInd.iloc[N:noDays-n,2]
        testX[0:,1] = bbInd.iloc[N:noDays-n,4]
        testX[0:,2] = macdInd.iloc[N:noDays-n,4]

        res = self.learner.query(testX)

        days = prices.index[N:noDays-n]
        order = pd.DataFrame(index=days,columns=['Symbol','Order','Shares'])
        hold = 0

        noActions = 0
        for i in range(noDays-N-n):
            if hold==0 and res[i]>0:
                order.iloc[i] = [symbol, 'BUY', 1000]
                hold = 1000
                noActions+=1
            elif hold==0 and res[i]<0:
                order.iloc[i] = [symbol, 'SELL', 1000]
                hold = -1000
                noActions+=1
            elif hold==-1000 and res[i]>0:
                order.iloc[i] = [symbol,'BUY',2000]
                hold = 1000
                noActions+=1
            elif hold==1000 and res[i]<0:
                order.iloc[i] = [symbol,'SELL',2000]
                hold = -1000
                noActions+=1
        #print(noActions)

        order = order.dropna(axis=0,how='any')
        return order
