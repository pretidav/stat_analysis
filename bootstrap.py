import numpy as np
import random 

class bootstrap():
    def __init__(self,data,Nb,block=None):
        self.data = data 
        self.Nb   = Nb
        self.block = block

    def sample(self):
        if self.block != None:
            self.data = self.data[:int(self.block*np.floor(len(self.data)/self.block))]
            self.data = np.mean(self.data.reshape(-1, self.block), axis=1)   
        dd = np.zeros((len(self.data),self.Nb+1))
        dd[:,0] = self.data
        for i in range(1,self.Nb+1):
            dd[:,i] = random.choices(self.data, k=len(self.data))
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
            M[:,i]=np.random.normal(0, 1, self.Nb)
        if len(self.k)>1:
            M = np.dot(M,np.linalg.cholesky(self.cov).T)
        else : 
            M = M * cov
        for i in range(len(self.k)):
            kdummy    = M[:,i] + k[i]
            kBS[0,i]  = k[i]
            kBS[1:,i] = kdummy 
            del kdummy
        return kBS

if __name__=='__main__':

    k = [2,3]
    cov = [[0.3,0.5],[0.5,2]]
    print('cov:')
    print(cov)
    print('k:')
    print(k)
    BS=synt_bootstrap(k=k,Nb=10000000,cov=cov)
    b=BS.sample()
    print('check cov:')
    print(np.cov(b.T))
    print('check k:')
    print(np.mean(b,axis=0))


    k = [2]
    cov = [0.3]
    print('std:')
    print(cov)
    print('k:')
    print(k)
    BS=synt_bootstrap(k=k,Nb=10000000,cov=cov)
    b=BS.sample()
    print('check std:')
    print(np.sqrt(np.cov(b.T)))
    print('check k:')
    print(np.mean(b,axis=0))