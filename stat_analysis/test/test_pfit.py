import numpy as np
from pfit import pfit
import unittest


class TestLinearFit(unittest.TestCase):
    def test_fit(self):
      np.random.seed(0)
      x = np.linspace(0,10,num=10)
      y = 5*x**2+ 2*x + 5 + 0.1*np.random.rand(len(x))
      dy = 100*np.random.rand(len(x))
      ff = pfit(x=x,y=y,dy=dy,ndeg=2)
      ff.fit()
      self.assertTrue(ff.k[0]-5<10**-1,"fit parameter wrong")
      self.assertTrue(ff.k[1]-2<10**-1,"fit parameter wrong")
      self.assertTrue(ff.k[2]-5<10**-1,"fit parameter wrong")
       
if __name__=='__main__':
    unittest.main()
    