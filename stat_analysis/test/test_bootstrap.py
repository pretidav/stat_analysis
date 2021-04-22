import numpy as np
from bootstrap import synt_bootstrap, bootstrap
import unittest


class TestBootstrap(unittest.TestCase):
    def test_multiple_parameters(self):
        k = [2,3]
        cov = [[0.3,0.5],[0.5,2]]
        np.random.seed(0)
        BS=synt_bootstrap(k=k,Nb=1000000,cov=cov)
        b=BS.sample()
        self.assertTrue(np.sum(k-np.mean(b,axis=0))<10**-4, "difference params should be <10**-6") 
        self.assertTrue(np.sum(np.cov(b.T)-cov)<10**-4, "difference in cov should be <10**-6") 
    
    def test_single_parameter(self):
        k = [2]
        cov = [0.3]
        np.random.seed(0)
        BS=synt_bootstrap(k=k,Nb=100000,cov=cov)
        b=BS.sample()
        self.assertTrue(np.sum(k-np.mean(b,axis=0))<10**-4, "difference params should be <10**-6") 
        self.assertTrue(np.sum(np.sqrt(np.cov(b.T))-cov)<10**-4, "difference in cov should be <10**-6") 
    
if __name__=='__main__':
    unittest.main()