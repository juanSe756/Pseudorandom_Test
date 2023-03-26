import numpy as np
from scipy.stats import norm
class MeanTest:
    def __init__(self, acceptance_lvl=0.05):
        self.acceptance_lvl = acceptance_lvl
    
    """"Main method to make test"""
    def evaluate(self, data):
        self.n = len(data) # number of samples
        self.m = np.mean(data) #get mean of data
        self.v = np.std(data) #get standard
        pb_acum = 1-(self.acceptance_lvl/2)
        z = norm.ppf(pb_acum)
        self.li = (1/2) - z * (1/ np.sqrt(12 * self.n)) #Lower bound calculation
        self.ls = (1/2) + z * (1/ np.sqrt(12 * self.n)) #Higher bound calculation
        return self.discriminate_nums(self.li,self.ls,data), self.getFrequences(data), self.n
    
    """"Reject or approve numbers"""
    def discriminate_nums(self,li,ls,data):
        approved_nums=[]
        for i in data:
            if(li<i<ls): #if the number is between li and ls, it's accepted
                approved_nums.append(i)
        return approved_nums
    
    """"Get the times Ni is in the sample"""
    def getFrequences(self,data):
        freq=[]
        ni,maximum,minimum = self.getNi(data)
        interval = minimum #First interval is equal to the minium data
        freq.append(ni.count(interval))
        bins=int(1+np.log2(self.n)) #Number of intervals to calculate
        i=0
        while i!=bins:
            temp_interv = interval+(maximum-minimum)/bins #Frequency for every interval
            freq.append(ni.count(temp_interv)) #add the frequency to frequencies array
            interval=temp_interv
            i+=1
        return freq
    
    """"Calculate the Ni for every Ri"""
    def getNi(self,data):
        ni=[] 
        for ri in data:
            ni.append(norm.ppf(ri)) #INV.NORM.ESTAND 
            # ni.append(norm.ppf(ri,np.mean(data),np.std(data))) #NORM.INV
        return ni,max(ni),min(ni) 
    
    """"Get Mean and Std of the sample"""
    def getMeanAndStd(self):
        return self.m, self.v
    