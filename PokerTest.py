import numpy as np
from scipy.stats import chi2
class PokerTest:
    def __init__(self, acceptance_lvl=0.05):
        self.acceptance_lvl = acceptance_lvl
        self.Oi=[0,0,0,0,0,0,0] #Observed freq
        self.prob = [0.30240, 0.50400, 0.10800, 0.07200, 0.00900, 0.00450, 0.00010] #Theorical prob for every hand

    """"Main method to make test"""
    def evaluate(self, data):
        n=len(data) #Number of samples
        for i in data:
            num="{:.5f}".format(i) #We must truncate the number to be able to count its digits
            truncated_num = float(num) #Cast to float
            num=str(truncated_num).replace('0.','') #We don't need 0 or . characters so we remove them
            self.tipo(num) #Clasificate every number of data
        Ei=[]
        for j in self.prob:
            Ei.append(j*n) #We multipy every prob by number of samples

        finals=[]
        k=0
        for h in Ei:
            finals.append(((h-self.Oi[k])**2)/h) #Finally, we apply the formula to get the values
            k+=1
        #Save the amount for every hand to be able to show them after
        counts=f"D: {self.Oi[0]} O: {self.Oi[1]} T: {self.Oi[2]} K: {self.Oi[3]} F: {self.Oi[4]} \n P: {self.Oi[5]} Q: {self.Oi[6]}"
        return chi2.ppf(0.05, 6), counts, np.sum(finals),n,self.Oi, Ei 
    
    """Evaluate if the number has 5 same digits"""
    def flushQ(self,number):
        digit1 = number[0]
        for digit in number:
            if digit != digit1:
                return False
        return True
    
    """Evaluate if the number has 3 same digits and one pair same"""
    def fullHouseF(self,number):
        # count
        guide = dict.fromkeys(number, 0)
        for digit in number:
            guide[digit]+=1
        if(2 in guide.values() and 3 in guide.values()):
            return True
        return False
    
    """Evaluate if the number has 4 same digits"""
    def pokerP(self,number):
        if(self.kindK(number)):
            # count
            guide = dict.fromkeys(number, 0)
            for digit in number:
                guide[digit]+=1
            for count in guide.values():
                if count >= 4:
                    return True
            return False
        else:
            return False
    """Evaluate if the number has 3 same digits"""
    def kindK(self,number):
        # count
        guide = dict.fromkeys(number, 0)
        for digit in number:
            guide[digit]+=1
        # Impair
        for count in guide.values():
            if count >= 3:
                return True
        return False
    
    """Evaluate if the number has 1 pair of same digits"""
    def onePairO(self,number):
        # count
        guide = dict.fromkeys(number, 0)
        for digit in number:
            guide[digit]+=1
        # pair
        for count in guide.values():
            if count >= 2:
                return True
        return False
    
    """Evaluate if the number has 2 pair of same digits"""
    def twoPairsT(self,number):
        # count
        guide = dict.fromkeys(number, 0)
        for digit in number:
            guide[digit]+=1
        # First pair
        # Only if we know there's one
        if self.onePairO(number):
            pair = None
            for count in guide.items():
                if count[1] >= 2:
                    pair = count[0]
                    break
            # We removed the one that was
            del guide[pair]
            # Second pair
            for count in guide.values():
                if count >= 2:
                    return True
            return False
        else:
            return False
    
    """Evaluate if all the digits are different"""
    def td(self,number):
        return not (len(number) != len(set(number)))
    
    """Evaluate the number to count poker hands and save the amount result for every hand"""
    def tipo(self,number):
        if self.flushQ(number):
            self.Oi[6]+=1
        elif self.pokerP(number):
            self.Oi[5]+=1
        elif self.fullHouseF(number):
            self.Oi[4]+=1
        elif self.kindK(number):
            self.Oi[3]+=1
        elif self.twoPairsT(number):
            self.Oi[2]+=1
        elif self.onePairO(number):
            self.Oi[1]+=1
        else:
            self.Oi[0]+=1
