import numpy as np
from comparator import comparator
import unittest


class TestBootstrap(unittest.TestCase):
    def test_same_distro(self):
      np.random.seed(0)
      a = np.random.normal(2,3,5000)
      b = np.random.normal(2,3,1000)
      aa = comparator(A=a,B=b,normaltest=True)
      self.assertFalse(aa.compare(),"stat test are failing")

    def test_different_distro(self):
      np.random.seed(0)
      a = np.random.normal(1,2,5000)
      b = np.random.normal(2,3,1000)
      aa = comparator(A=a,B=b,normaltest=True)
      self.assertTrue(aa.compare(),"stat test are failing")
      
    def test_normal_distro(self):
      np.random.seed(0)
      a = np.random.rand(1000)
      b = np.random.rand(500)
      aa = comparator(A=a,B=b,normaltest=True)
      self.assertFalse(aa.compare(),"normal test is failing")
      

if __name__=="__main__":
    unittest.main()
