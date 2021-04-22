import numpy as np
from nlfit import nlfit
import unittest


class TestNonLinFit(unittest.TestCase):
    def test_fit(self):
      def f(B, x):
            return np.exp(B[0]*x) + B[1]*np.sin(x) + B[2] 
      
      np.random.seed(0)
      x = np.linspace(0,10,num=20)
      y = f([0.2,1,5],x) + 0.01*np.random.rand(len(x))
      dy = 0.05*np.random.rand(len(x))
      dx = 0.05*np.random.rand(len(x))

      ff = nlfit(func=f,x=x,y=y,dx=dx,dy=dy,k0=[0.,0.,0.])
      ff.fit()

      self.assertTrue(ff.fitout.beta[0]-0.2<10**-1,"fit parameter wrong")
      self.assertTrue(ff.fitout.beta[1]-1<10**-1,"fit parameter wrong")
      self.assertTrue(ff.fitout.beta[2]-5<10**-1,"fit parameter wrong")
      
if __name__=='__main__':
  unittest.main()
  