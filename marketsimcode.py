"""MC2-P1: Market simulator."""
## Taiyu Guo
## GTID: 903256162, username: tguo40
import pandas as pd
import numpy as np
import datetime as dt
import os
import sys
sys.path.append("../")
from util import get_data, plot_data

def author():
        return 'tguo40' # replace tb34 with your Georgia Tech username.

def compute_portvals(order, start_date, end_date, start_val = 1000000, commission=9.95, impact=0.005):
    n = len(order)
    dates = pd.date_range(order.index[0],end_date)
    spy = get_data(['SPY'],dates);

    portvals = pd.DataFrame(index=spy.index)
    portvals.insert(loc=0, column='Value of Portfolio', value = np.zeros(len(portvals.index)))

    cash = start_val

    portfolio = pd.DataFrame(index=order.index,columns=np.unique(order['Symbol']),data=np.zeros((n,len(np.unique(order['Symbol'])))))
    portfolio.insert(loc=0,column='cash',value=np.zeros(len(portfolio.index)))

    for i in range(0,n):
        sym = order['Symbol'].ix[i]
        date = order.index[i];
        stock = get_data([sym],pd.date_range(date,date))
        while len(stock) == 0:
            date = date + dt.timedelta(days=1);
            stock = get_data([sym],pd.date_range(date,date))
            portfolio = pd.DataFrame(index=[date],columns=np.unique(order['Symbol']),data=np.zeros((n,len(np.unique(order['Symbol'])))))
            portfolio.insert(loc=0,column='cash',value=np.zeros(len(portfolio.index)))

        price = stock[sym].ix[0]
        noShares = order['Shares'].ix[i]

        if order['Order'].ix[i]=='BUY':
            cash = cash - (1+impact)*price*noShares - commission
            portfolio[sym].ix[i:] = portfolio[sym].ix[i:]+noShares
            portfolio['cash'].ix[i] = cash

        elif order['Order'].ix[i]=='SELL':
            cash = cash + (1-impact)*price*noShares - commission
            portfolio[sym].ix[i:] = portfolio[sym].ix[i:]-noShares
            portfolio['cash'].ix[i] = cash
    portfolio = portfolio[~portfolio.index.duplicated(keep='last')]
    #print(portfolio)
    idx = 0
    nDays = len(portvals)

    for i in range(0,nDays):
        currDate = portvals.index[i]
        portDate = portfolio.index[idx]
        stocks = portfolio.columns[1:]

        if (idx+1<nDays and currDate>=portDate and (len(portfolio.index)==1 or idx+1 ==len(portfolio.index) or currDate<portfolio.index[idx+1])):
            cash = portfolio['cash'].ix[idx]
            total = cash
            for sym in stocks:
                no_Shares = portfolio[sym].ix[idx]
                if (no_Shares != 0.0):
                    stck  = get_data([sym], pd.date_range(currDate,currDate))
                    pr = stck[sym].ix[0]
                    total = total + no_Shares*pr
            portvals.ix[currDate] = total
        else:
            idx=idx+1
            #print(portvals)
            cash = portfolio['cash'].ix[idx]
            total = cash
            for sym in stocks:
                no_Shares = portfolio[sym].ix[idx]
                if (no_Shares != 0.0):
                    stck  = get_data([sym], pd.date_range(currDate,currDate))
                    pr = stck[sym].ix[0]
                    total = total + no_Shares*pr
                portvals.ix[currDate] = total
    # print(portvals)
    return portvals
