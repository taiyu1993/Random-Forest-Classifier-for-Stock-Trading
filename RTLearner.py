"""
A simple wrapper for Random Tree Learner.  (c) 2017 Taiyu Guo
"""
## Taiyu Guo
## GTID: 903256162, username: tguo40
import numpy as np
import random
from scipy import stats

class RTLearner(object):

    def __init__(self, leaf_size = 1,verbose = False):
        self.leaf_size = leaf_size
        self.tree = {}

    def author(self):
        return 'tguo40' # replace tb34 with your Georgia Tech username

    def computeBestFeature(self,dataX,dataY):
	    num_feat = dataX.shape[1]
	    return np.random.randint(num_feat-1)

    def buildTree(self,dataX,dataY):
	    #print len(dataY)
        nrow = dataX.shape[0]
        ncol = dataX.shape[1]

        if(nrow <= self.leaf_size):
            mode = stats.mode(dataY,axis=0)
            #print(mode[0][0])
            return mode[0][0]

        if(len(np.unique(dataY))==1):
            mode = stats.mode(dataY,axis=0)
            #print(mode[0][0])
            return mode[0][0]

	    #randomly compute best_feature and split_value
        best_feature=self.computeBestFeature(dataX,dataY)

        r1 = np.random.randint(nrow)
        r2 = np.random.randint(nrow)
        split_value = (dataX[r1,best_feature]+dataX[r2,best_feature])/2
        left = dataX[dataX[:,best_feature] <= split_value].shape[0]
        right = dataX[dataX[:,best_feature] > split_value].shape[0]

        if left == 0 or right == 0:
            split_value = np.mean(dataX[:,best_feature])

        true_rowsX = dataX[dataX[:,best_feature] <= split_value]
        true_rowsY = dataY[dataX[:,best_feature] <= split_value]
        false_rowsX = dataX[dataX[:,best_feature] > split_value]
        false_rowsY = dataY[dataX[:,best_feature] > split_value]

        true_branch = self.buildTree(true_rowsX,true_rowsY)
        false_branch = self.buildTree(false_rowsX,false_rowsY)

        return {"split_value":split_value, "best_feature":best_feature, "true_branch":true_branch, "false_branch":false_branch}


    def addEvidence(self,dataX,dataY):
        self.tree = self.buildTree(dataX,dataY)

    def query(self,query_points):
        num_pred = query_points.shape[0]
        pred = np.zeros(num_pred)
        tree = self.tree

        for i in range(0,num_pred):
            traverse = tree
            while(not isinstance(traverse,float)):
                feature = traverse["best_feature"]
                if(query_points[i][feature]<=traverse["split_value"]):
                    traverse = traverse["true_branch"]
                else:
                    traverse = traverse["false_branch"]
            pred[i] = traverse
        return pred

if __name__=="__main__":
    print("the secret clue is 'zzyzx'")
