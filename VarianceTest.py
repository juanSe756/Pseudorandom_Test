import numpy as np
from scipy.stats import chi2

class VarianceTest:
    def __init__(self, acceptance_lvl=0.05):
        self.acceptance_lvl = acceptance_lvl

    """"Main method to make test"""
    def evaluate(self, data):
        n = len(data) # number of samples
        r = np.mean(data) # get mean of data
        self.var = np.var(data) # get variance of data
        p1 = self.acceptance_lvl/2 #𝝈^𝟐 Variance of data
        p2 = 1-(self.acceptance_lvl/2) #𝜶/𝟐 
        self.x1 =chi2.isf(p1,n-1) #𝑿_(𝜶/𝟐)^𝟐
        self.x2 = chi2.isf(p2, n-1) #𝑿_(𝟏−(𝜶/𝟐))^𝟐
        self.li = self.x1/(12*(n-1)) #lower bound
        self.ls = self.x2/(12*(n-1)) #Higher bound
        return self.valid(), n, self.discriminate_nums(self.li,self.ls,data), self.li, self.ls
    
    """"Reject or approve numbers"""
    def discriminate_nums(self,li,ls,data):
        approved_nums=[]
        for i in data:
            if(ls<i<li): #if the number is between li and ls, it's accepted
                approved_nums.append(i) 
        return approved_nums
    
    """Evaluate if variance of data is between li and ls, if it is, it passes the test"""
    def valid(self):
        return self.ls<self.var<self.li
