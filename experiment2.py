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

    learner1 = sl.StrategyLearner(verbose=False,impact=0)
    learner2 = sl.StrategyLearner(verbose=False,impact=0.001)
    learner3 = sl.StrategyLearner(verbose=False,impact=0.0025)
    learner4 = sl.StrategyLearner(verbose=False,impact=0.005)
    learner5 = sl.StrategyLearner(verbose=False,impact=0.01)
    learner6 = sl.StrategyLearner(verbose=False,impact=0.02)

    learner1.addEvidence(symbol="JPM",sd=sd,ed=ed,sv=sv)
    learner2.addEvidence(symbol="JPM",sd=sd,ed=ed,sv=sv)
    learner3.addEvidence(symbol="JPM",sd=sd,ed=ed,sv=sv)
    learner4.addEvidence(symbol="JPM",sd=sd,ed=ed,sv=sv)
    learner5.addEvidence(symbol="JPM",sd=sd,ed=ed,sv=sv)
    learner6.addEvidence(symbol="JPM",sd=sd,ed=ed,sv=sv)

    orderStrat1 = learner1.test(symbol="JPM",sd=sd,ed=ed,sv=sv)
    orderStrat2 = learner2.test(symbol="JPM",sd=sd,ed=ed,sv=sv)
    orderStrat3 = learner3.test(symbol="JPM",sd=sd,ed=ed,sv=sv)
    orderStrat4 = learner4.test(symbol="JPM",sd=sd,ed=ed,sv=sv)
    orderStrat5 = learner5.test(symbol="JPM",sd=sd,ed=ed,sv=sv)
    orderStrat6 = learner6.test(symbol="JPM",sd=sd,ed=ed,sv=sv)

    portStrat1 = compute_portvals(order=orderStrat1,start_date=sd,end_date=ed,start_val=sv,commission=0,impact=0)
    portStrat2 = compute_portvals(order=orderStrat2,start_date=sd,end_date=ed,start_val=sv,commission=0,impact=0.001)
    portStrat3 = compute_portvals(order=orderStrat3,start_date=sd,end_date=ed,start_val=sv,commission=0,impact=0.0025)
    portStrat4 = compute_portvals(order=orderStrat4,start_date=sd,end_date=ed,start_val=sv,commission=0,impact=0.005)
    portStrat5 = compute_portvals(order=orderStrat5,start_date=sd,end_date=ed,start_val=sv,commission=0,impact=0.01)
    portStrat6 = compute_portvals(order=orderStrat6,start_date=sd,end_date=ed,start_val=sv,commission=0,impact=0.02)

    noDays=len(portStrat1.index)
    cr_bm = (portStrat1.iloc[noDays-1]/portStrat1.iloc[0])-1
    dr_bm = portStrat1 / portStrat1.shift(1)-1
    adr_bm = dr_bm.mean()
    sddr_bm = dr_bm.std()
    sr_bm =(252)**(.5)*(dr_bm).mean()/(dr_bm).std()
    ev_bm = portStrat1.iloc[noDays-1]
    print("Cumulative Return:", cr_bm)
    print("Std Dev DR:", sddr_bm)
    print("Average Daily Return", adr_bm)
    print("Sharpe Ratio", sr_bm)
    print("End Value:", ev_bm)
    print(" ")

    noDays=len(portStrat2.index)
    cr_bm = (portStrat2.iloc[noDays-1]/portStrat2.iloc[0])-1
    dr_bm = portStrat2 / portStrat2.shift(1)-1
    adr_bm = dr_bm.mean()
    sddr_bm = dr_bm.std()
    sr_bm =(252)**(.5)*(dr_bm).mean()/(dr_bm).std()
    ev_bm = portStrat2.iloc[noDays-1]
    print("Cumulative Return:", cr_bm)
    print("Std Dev DR:", sddr_bm)
    print("Average Daily Return", adr_bm)
    print("Sharpe Ratio", sr_bm)
    print("End Value:", ev_bm)
    print(" ")

    noDays=len(portStrat3.index)
    cr_bm = (portStrat3.iloc[noDays-1]/portStrat3.iloc[0])-1
    dr_bm = portStrat3 / portStrat3.shift(1)-1
    adr_bm = dr_bm.mean()
    sddr_bm = dr_bm.std()
    sr_bm =(252)**(.5)*(dr_bm).mean()/(dr_bm).std()
    ev_bm = portStrat3.iloc[noDays-1]
    print("Cumulative Return:", cr_bm)
    print("Std Dev DR:", sddr_bm)
    print("Average Daily Return", adr_bm)
    print("Sharpe Ratio", sr_bm)
    print("End Value:", ev_bm)
    print(" ")

    noDays=len(portStrat4.index)
    cr_bm = (portStrat4.iloc[noDays-1]/portStrat4.iloc[0])-1
    dr_bm = portStrat4 / portStrat4.shift(1)-1
    adr_bm = dr_bm.mean()
    sddr_bm = dr_bm.std()
    sr_bm =(252)**(.5)*(dr_bm).mean()/(dr_bm).std()
    ev_bm = portStrat4.iloc[noDays-1]
    print("Cumulative Return:", cr_bm)
    print("Std Dev DR:", sddr_bm)
    print("Average Daily Return", adr_bm)
    print("Sharpe Ratio", sr_bm)
    print("End Value:", ev_bm)
    print(" ")

    noDays=len(portStrat5.index)
    cr_bm = (portStrat5.iloc[noDays-1]/portStrat5.iloc[0])-1
    dr_bm = portStrat5 / portStrat5.shift(1)-1
    adr_bm = dr_bm.mean()
    sddr_bm = dr_bm.std()
    sr_bm =(252)**(.5)*(dr_bm).mean()/(dr_bm).std()
    ev_bm = portStrat5.iloc[noDays-1]
    print("Cumulative Return:", cr_bm)
    print("Std Dev DR:", sddr_bm)
    print("Average Daily Return", adr_bm)
    print("Sharpe Ratio", sr_bm)
    print("End Value:", ev_bm)
    print(" ")

    noDays=len(portStrat6.index)
    cr_bm = (portStrat6.iloc[noDays-1]/portStrat6.iloc[0])-1
    dr_bm = portStrat6 / portStrat6.shift(1)-1
    adr_bm = dr_bm.mean()
    sddr_bm = dr_bm.std()
    sr_bm =(252)**(.5)*(dr_bm).mean()/(dr_bm).std()
    ev_bm = portStrat6.iloc[noDays-1]
    print("Cumulative Return:", cr_bm)
    print("Std Dev DR:", sddr_bm)
    print("Average Daily Return", adr_bm)
    print("Sharpe Ratio", sr_bm)
    print("End Value:", ev_bm)
    print(" ")

    df_new = pd.concat([portStrat1,portStrat2,portStrat3,portStrat4,portStrat5,portStrat6],axis=1)
    df_new=df_new.fillna(value=sv,axis=1)
    df_new.columns = ['impact=0','impact=0.001','impact=0.0025','impact=0.005','impact=0.01','impact=0.02']

    df_new = df_new/df_new.iloc[0,:]
    graph = df_new.plot(color=['green','blue','red','black','chocolate','aqua'],linewidth=0.8)
    graph.set_xlabel('Date')
    graph.set_ylabel('Normalized Portfolio value')
    plt.grid(linestyle='dotted')
    plt.title("Portfolio values for various impact values")
    fmt = mdates.DateFormatter("%b %Y")
    graph.xaxis.set_major_formatter(fmt)
    plt.show()

if __name__ == "__main__":
    main()
