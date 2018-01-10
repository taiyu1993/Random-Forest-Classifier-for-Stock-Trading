"""
A simple wrapper for Bag Learner.  (c) 2017 Taiyu Guo
"""
## Taiyu Guo
## GTID: 903256162, username: tguo40
import numpy as np
import random
from scipy import stats

class BagLearner(object):
    def __init__(self, learner, kwargs, bags, boost=False, verbose = False):
        self.learner = learner
        self.args = kwargs
        self.bag_size = bags
        self.boost = boost
        self.bag=[]
        for i in range(0,bags):
            self.bag.append(self.learner(**self.args))

    def author(self):
        return 'tguo40' #replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        ncol = dataX.shape[0]
        index = np.arange(0,ncol)

        for i in range(self.bag_size):
            sample_index = np.random.choice(index,ncol,replace = True)
            sample_X = dataX[sample_index]
            sample_Y = dataY[sample_index]
            self.bag[i].addEvidence(sample_X,sample_Y)

    def query(self,query_points):
        nrows = query_points.shape[0]
        predY = np.zeros(nrows)
        # generate predictions by all predictors in bag
        bagY = np.zeros((nrows,self.bag_size))

        for i in range(self.bag_size):
            bagY[:,i] = self.bag[i].query(query_points)

        for i in range(0,nrows):
            mode = stats.mode(bagY[i,:],axis=0)
            predY[i] = mode[0][0]

        return predY
