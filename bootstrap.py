import numpy as np

class bootstrap():
    def __init__(self,data,Nb,block=None):
        self.data = data 
        self.Nb   = Nb
        self.block = block

    def sample(self):
        if self.block != None:
            self.data = self.data[:self.block*np.floor(len(self.data)/self.block)]
            self.data = np.mean(self.data.reshape(-1, self.block), axis=1)   
        dd = np.zeros((len(self.data),self.Nb+1))
        dd[:,0] = self.data
        for i in range(1,self.Nb):
            dd[:,i] = np.random.choices(self.data, k=len(self.data))
        return dd

class synt_bootstrap():
    def __init__(self,k,Nb,cov):
        self.k   = k 
        self.Nb  = Nb
        self.cov = cov 

    def sample(self):
        M   = np.zeros((self.Nb,len(self.k)))
        kBS = np.zeros((self.Nb+1,len(self.k)))         
        for i in range(len(self.k)):
            M[:,i]=np.random.normal(self.Nb,1)
        M = np.dot(M,np.linalg.cholesky(self.cov))
        for i in range(len(self.k)):
            del kdummy
            kdummy    = M[:,i] + k[i]
            kBS[1,i]  = k[i]
            kBS[1:,i] = kdummy 
        return kBS