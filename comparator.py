from scipy.stats import normaltest, ttest_ind, ks_2samp
import numpy as np
import matplotlib.pyplot as plt

class comparator():
  def __init__(self,A,B,confidence=0.05):
    self.A = A
    self.B = B
    self.confidence = confidence
    self.get_stat()
    self.log()

  def get_stat(self):
    self.muA = np.mean(self.A)
    self.muB = np.mean(self.B)
    self.stdA = np.std(self.A)
    self.stdB = np.std(self.B)
    self.sterrA = self.stdA/np.sqrt(len(self.A))
    self.sterrB = self.stdB/np.sqrt(len(self.B))

  def log(self,n=20):
    self.n = n
    self.string = ' Log '
    print('='*self.n + self.string + '='*self.n)
    print('A        = {}'.format(self.muA))
    print('std A    = {}'.format(self.stdA))
    print('sterr A  = {}'.format(self.sterrA))
    print('B        = {}'.format(self.muB))
    print('std B    = {}'.format(self.stdB))
    print('sterr B  = {}'.format(self.sterrB))
    print('='*self.n + '='*len(self.string) + '='*self.n)

  def plot(self,bins=50,savename=None):
    plt.hist(self.A,alpha=0.5,density=True)
    plt.hist(self.B,alpha=0.5,density=True)
    plt.legend(['A','B'],loc='best')
    plt.axvline(self.muA, color='blue', linestyle='dashed', linewidth=1)
    plt.axvline(self.muB, color='orange', linestyle='dashed', linewidth=1)
    if savename!=None:
        plt.savefig(fname=savename)
    else:
        plt.show()

  def compare(self):
    _, pA = normaltest(self.A)
    _, pB = normaltest(self.B)
    self.diff = None
    passed = True
    if pA > self.confidence:
      print('A - normal test:           PASSED')
    else : 
      print('A - normal test: NOT PASSED')
      passed = False
    if pB > self.confidence:
      print('B - normal test:           PASSED')
    else :
      print('B - normal test: NOT PASSED')
      passed = False

    if passed: 
      _, p_test = ttest_ind(self.A, self.B, equal_var=False)
      if p_test < self.confidence:
        print("Welch's t-test:            PASSED") 
        diff_W = True
      else : 
        print("Welch's t-test:          NOT PASSED") 
        diff_W = False 

      _, p_test2 = ks_2samp(self.A, self.B)
      if p_test < self.confidence:
        diff_KS = True
        print("Kolmogorov-Smirnov test:   PASSED")
      else : 
        print("Kolmogorov-Smirnov test: NOT PASSED") 
        diff_KS = False 
      
      print('='*self.n + '='*len(self.string) + '='*self.n)
      if diff_KS and diff_W:
        print('A and B are significantly different with {}% confidence'.format((1-self.confidence)*100)) 
      else :
        print('A and B are from the same distribution with {}% confidence'.format((1-self.confidence)*100)) 
    else : 
      print('Error: distributions are not normal - more measurements are required')

if __name__=="__main__":
    a = np.random.normal(2,0.2,100)
    b = np.random.normal(2.1,0.2,100)

    aa = comparator(A=a,B=b)
    aa.compare()
    aa.plot(bins=100,savename='david.png')