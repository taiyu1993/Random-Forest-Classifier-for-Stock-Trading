## Taiyu Guo
## GTID: 903256162, username: tguo40

import StrategyLearner as sl
from marketsimcode import compute_portvals
import ManualStrategy as ms
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def main():
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    sv= 100000

    dates = pd.date_range(sd, ed)
    noDays = len(dates)

    learner = sl.StrategyLearner(verbose=False,impact=0.0)
    learner.addEvidence(symbol="JPM",sd=sd,ed=ed,sv=sv)
    orderStrat = learner.test(symbol="JPM",sd=sd,ed=ed,sv=sv)
    portStrat = compute_portvals(order=orderStrat,start_date=sd,end_date=ed,start_val=sv,commission=0,impact=0)

    manSt = ms.ManualStrategy()
    portBM, portManual = manSt.testPolicy(symbol='JPM',sd=sd,ed=ed,sv=sv)

    # compute stats for benchmark

    print("Benchmark:")
    noDays = len(portBM.index)
    cr_bm = (portBM.iloc[noDays-1]/portBM.iloc[0])-1
    dr_bm = portBM / portBM.shift(1)-1
    adr_bm = dr_bm.mean()
    sddr_bm = dr_bm.std()
    sr_bm =(252)**(.5)*(dr_bm).mean()/(dr_bm).std()
    ev_bm = portBM.iloc[noDays-1]
    print("Cumulative Return:", cr_bm)
    print("Std Dev DR:", sddr_bm)
    print("Average Daily Return", adr_bm)
    print("Sharpe Ratio", sr_bm)
    print("End Value:", ev_bm)
    print(" ")

    print("Manual:")
    noDays=len(portManual.index)
    cr_bm = (portManual.iloc[noDays-1]/portManual.iloc[0])-1
    dr_bm = portManual / portManual.shift(1)-1
    adr_bm = dr_bm.mean()
    sddr_bm = dr_bm.std()
    sr_bm =(252)**(.5)*(dr_bm).mean()/(dr_bm).std()
    ev_bm = portManual.iloc[noDays-1]
    print("Cumulative Return:", cr_bm)
    print("Std Dev DR:", sddr_bm)
    print("Average Daily Return", adr_bm)
    print("Sharpe Ratio", sr_bm)
    print("End Value:", ev_bm)
    print(" ")

    print("Strategy:")
    noDays=len(portStrat.index)
    cr_bm = (portStrat.iloc[noDays-1]/portStrat.iloc[0])-1
    dr_bm = portStrat / portStrat.shift(1)-1
    adr_bm = dr_bm.mean()
    sddr_bm = dr_bm.std()
    sr_bm =(252)**(.5)*(dr_bm).mean()/(dr_bm).std()
    ev_bm = portStrat.iloc[noDays-1]
    print("Cumulative Return:", cr_bm)
    print("Std Dev DR:", sddr_bm)
    print("Average Daily Return", adr_bm)
    print("Sharpe Ratio", sr_bm)
    print("End Value:", ev_bm)
    print(" ")

    df_new = pd.concat([portBM,portManual,portStrat],axis=1)
    df_new=df_new.fillna(value=sv,axis=1)
    df_new.columns = ['Benchmark','Manual','Strategy']

    df_new = df_new/df_new.iloc[0,:]
    graph = df_new.plot(color=['green','blue','red'],linewidth=0.8)
    graph.set_xlabel('Date')
    graph.set_ylabel('Normalized Portfolio value')
    plt.grid(linestyle='dotted')
    plt.title("Portfolio values for Benchmark vs Manual Strategy and StrategyLearner")
    fmt = mdates.DateFormatter("%b %Y")
    graph.xaxis.set_major_formatter(fmt)
    plt.show()

if __name__ == "__main__":
    main()
