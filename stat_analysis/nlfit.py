import numpy as np
from scipy import odr, stats
import matplotlib.pyplot as plt
from stat_analysis.bootstrap import synt_bootstrap

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
    self.pred = None
    self.dpred = None

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
    print('{}'.format(self.fitout.cov_beta*self.fitout.res_var))
    if self.pred and self.dpred: 
      print(' k       = {}'.format(self.pred))
      print('dk       = {}'.format(self.dpred))    
    print('='*n + '='*len(string) + '='*n)

  def predict(self,x,savefile=None,xlabel=None,ylabel=None,Nb=5000):

    self.plot(savefile=None,xlabel=xlabel,ylabel=ylabel,Nb=Nb)

    extrapolation = False
    if x<min(self.x):
      px = np.linspace(x,min(self.x))
      extrapolation=True
    elif x>max(self.x):
      px = np.linspace(max(self.x),x)
      extrapolation=True
    
    if extrapolation:
      ff_ext = np.zeros((len(self.bs),len(px)))
      for i,mm in enumerate(self.bs): 
          ff_ext[i,:] = self.func(mm,px)
      f_ext = ff_ext[0,:]
      sf_ext = np.std(ff_ext[1:,:],axis=0)
      plt.fill_between(px,f_ext-sf_ext,f_ext+sf_ext,alpha=0.4,color='r')
      plt.plot(px,f_ext,'r--',linewidth=1)

    ff = np.zeros((len(self.bs),1))  
    for i,mm in enumerate(self.bs): 
      ff[i,:] = self.func(mm,x)
    self.dpred = np.std(ff[1:,:],axis=0)
    self.pred = ff[0,:]
    plt.errorbar(x=x,y=self.pred,yerr=self.dpred,fmt='gs')
    if savefile!=None:
      plt.savefig(fname=savefile)
  
    return {'pred':self.pred, 'dpred':self.dpred}

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
    self.bs = synt_bootstrap(k=self.fitout.beta,Nb=Nb,cov=self.fitout.cov_beta*self.fitout.res_var).sample()
    ff = np.zeros((Nb+1,len(px)))
    for i,mm in enumerate(self.bs): 
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
    dy = 1*np.random.rand(len(x))
    dx = 0.5*np.random.rand(len(x))

    ff = nlfit(func=f,x=x,y=y,dx=dx,dy=dy,k0=[0.,0.,0.])
    ff.fit()
    ff.plot(savefile='../fig/nonlin.png')
    plt.clf()
    ff.predict(x=10.5,xlabel='x',ylabel='y',savefile='../fig/nonlin_pred.png')
    ff.log()
