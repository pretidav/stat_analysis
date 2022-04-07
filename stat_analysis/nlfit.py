import numpy as np
from scipy import odr, stats
import matplotlib.pyplot as plt
from .bootstrap import synt_bootstrap

class nlfit():
  def __init__(self,func,x,y,k0,dx=None,dy=None):
    self.x = np.array(x) 
    self.y = np.array(y) 
    self.func = func
    self.k0   = k0 
    self.fitout = None
    self.dx = np.array(dx)
    self.dy = np.array(dy)
    self.t = None
    self.p_values = None

  def fit(self):
    model = odr.Model(self.func)
    
    mydata = odr.RealData(x=self.x, y=self.y, sx=self.dx, sy=self.dy)  
    self.fitout = odr.ODR(mydata, model, beta0=self.k0).run()
    self.t = self.fitout.beta/self.fitout.sd_beta
    self.dof = len(self.x)-len(self.k0)
    self.p_values =np.array([2*(1-stats.t.cdf(np.abs(i),self.dof)) for i in self.t])

  def log(self,n=20):
    string = ' Fit Log '
    print('='*n + string + '='*n)
    print(' k       = {}'.format(self.fitout.beta))
    print('dk       = {}'.format(self.fitout.sd_beta))
    print('t        = {}'.format(self.t))
    print('p-values = {}'.format(self.p_values))
    print('R**2     = {}'.format(self.fitout.sum_square))
    print('dof      = {}'.format(self.dof))
    print('cov      = ')
    print('{}'.format(self.fitout.cov_beta))
    print('='*n + '='*len(string) + '='*n)

  def plot(self,savefile=None,xlabel=None,ylabel=None,Nb=5000):
    if self.dy.any() and self.dx.any():
      plt.errorbar(x=self.x,y=self.y,yerr=self.dy,xerr=self.dx, fmt='bo')
    if self.dy.any() and not self.dx.any():
      plt.errorbar(x=self.x,y=self.y,yerr=self.dy, fmt='bo')
    if self.dx.any() and not self.dy.any():
      plt.errorbar(x=self.x,y=self.y,xerr=self.dx, fmt='bo')
    if not self.dy.any() and not self.dy.any():
      plt.errorbar(x=self.x,y=self.y,fmt='bo')

    px = np.linspace(min(self.x),max(self.x))
    bs = synt_bootstrap(k=self.fitout.beta,Nb=Nb,cov=self.fitout.cov_beta).sample()
    ff = np.zeros((Nb+1,len(px)))
    for i,mm in enumerate(bs): 
        ff[i,:] = self.func(mm,px)
    f  = ff[0,:]
    sf = np.std(ff[1:,:],axis=0) 
    plt.fill_between(px,f-sf,f+sf,alpha=0.4,color='r')
    plt.plot(px,f,'r--',linewidth=1)
    
    if xlabel!=None:
      plt.xlabel(xlabel,fontdict={'fontname':'Helvetica'})
    if ylabel!=None:
      plt.ylabel(ylabel,fontdict={'fontname':'Helvetica'})
    if savefile!=None:
      plt.savefig(fname=savefile)

if __name__=='__main__':
   
    def f(B, x):
        return np.exp(B[0]*x) + B[1]*np.sin(x) + B[2] 

    x = np.linspace(0,10,num=20)
    y = f([0.2,1,5],x) + 1*np.random.rand(len(x))
    dy = 4*np.random.rand(len(x))
    dx = 2*np.random.rand(len(x))

    ff = nlfit(func=f,x=x,y=y,dx=dx,dy=dy,k0=[0.,0.,0.])
    ff.fit()
    ff.log()
    ff.plot(savefile='nonlin.png')
