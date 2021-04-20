import numpy as np
import matplotlib.pyplot as plt 

import numpy as np
import matplotlib.pyplot as plt 


class pfit():
  def __init__(self,x,y,dy=None,ndeg=1,kconst=None):
    self.x = np.array(x)
    self.y = np.array(y)
    self.dy = np.array(dy)
    self.ndeg = int(ndeg)
    self.nconst = 0
    if kconst!=None:
      self.nconst = int(len(kconst)) 
    self.kconst = kconst
    self.cov        = None
    self.k          = None
    self.dof        = None
    self.chi2       = None
    self.dk         = None

  def fit(self):
    if self.dy.any():
      dy = self.dy
    else :
      dy = np.ones(len(y))
    yr = y/dy
    a = np.zeros(shape=(len(x),len(range(1,self.ndeg+1-self.nconst+1))))
    for n in range(1,self.ndeg+1-self.nconst+1):
      a[:,n-1] = (x**(self.ndeg-n+1))/dy
    a = np.dot(np.linalg.inv(np.dot(a.T,a)),a.T)
    self.k = np.dot(a,yr)
    self.cov = np.dot(a,a.T)
    self.dk = np.sqrt(np.diag(self.cov))
    fitr=0
    for n in range(1,self.ndeg+1-self.nconst+1):
      fitr+=((self.k[n-1])*x**(self.ndeg+1-n))/dy
    self.dof = (len(y)-self.ndeg-1+self.nconst)
    self.chi2 = np.sum((fitr-yr)**2)/self.dof
    if self.kconst!=None:
      self.k  = np.append(self.k,self.kconst)
      self.dk = np.append(self.dk,[0]*len(self.kconst))

  def stats(self):
    return self.k, self.dk, self.cov, self.chi2, self.dof

  def log(self,n=20):
    string = ' Fit Log '
    print('='*n + string + '='*n)
    print(' k       = {}'.format(self.k))
    print('dk       = {}'.format(self.dk))
    print('chi2/dof = {}'.format(self.chi2))
    print('dof      = {}'.format(self.dof))
    print('cov      = ')
    print('{}'.format(self.cov))
    print('='*n + '='*len(string) + '='*n)

  def plot(self,savefile=None,xlabel=None,ylabel=None):
    if self.dy.any():
      plt.errorbar(x=self.x,y=self.y,yerr=self.dy,fmt='bo')
    else :
      plt.errorbar(x=self.x,y=self.y,fmt='bo')

    px = np.linspace(min(self.x),max(self.x))
    a = np.zeros((len(px),len(range(1,self.ndeg+1-self.nconst+1))))
    err = np.zeros(len(px))
    for n in range(1,self.ndeg+1-self.nconst+1):
      a[:,n-1] = (px**(self.ndeg-n+1))
    for i in range(len(px)):
      err[i]=np.sqrt(np.dot(a[i,:],np.dot(self.cov,a[i,:].T)))
    
    f = np.zeros((len(px)))
    for ix in range(len(px)):
      for n in range(1,self.ndeg+1-self.nconst+1):
        f[ix]+=(self.k[n-1])*px[ix]**(self.ndeg+1-n)
    plt.plot(px,f,'r--',linewidth=1)
    plt.legend(['fit','data'],loc='best')
    
    plt.fill_between(px,f-err,f+err,alpha=0.4,color='r')
    if xlabel!=None:
      plt.xlabel(xlabel,fontdict={'fontname':'Helvetica'})
    if ylabel!=None:
      plt.ylabel(ylabel,fontdict={'fontname':'Helvetica'})
    if savefile!=None:
      plt.savefig(fname=savefile)

if __name__=='__main__':

    x = np.linspace(0,10,num=10)
    y = 4*x+ 2 + np.random.rand(len(x))
    dy = 30*np.random.rand(len(x))

    ff = pfit(x=x,y=y,dy=dy,ndeg=1,kconst=[2])
    ff.fit()
    ff.plot(xlabel='x',ylabel='y',savefile='test.eps')
    ff.log()