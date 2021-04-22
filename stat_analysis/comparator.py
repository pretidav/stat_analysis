from scipy.stats import normaltest, ttest_ind, ks_2samp
import numpy as np
import matplotlib.pyplot as plt

class comparator():
  def __init__(self,A,B,confidence=0.05,normaltest=True):
    self.A = A
    self.B = B
    self.confidence = confidence
    self.normaltest = normaltest
    self.get_stat()
    self.log()

  def get_stat(self):
    self.muA = np.mean(self.A)
    self.muB = np.mean(self.B)
    self.stdA = np.std(self.A)
    self.stdB = np.std(self.B)
    self.sterrA = float(self.stdA/np.sqrt(len(self.A)))
    self.sterrB = float(self.stdB/np.sqrt(len(self.B)))

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
    passed = True
    if self.normaltest:
      _, pA = normaltest(self.A)
      _, pB = normaltest(self.B)
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
      _, p_test0 = ttest_ind(self.A, self.B, equal_var=True)
      if p_test0 < self.confidence:
        print("Student's t-test:          PASSED p-value={}".format(p_test0)) 
        diff_S = True
      else : 
        print("Student's t-test:        NOT PASSED p-value={}".format(p_test0)) 
        diff_S = False 

      _, p_test1 = ttest_ind(self.A, self.B, equal_var=False)
      if p_test1 < self.confidence:
        print("Welch's t-test:            PASSED p-value={}".format(p_test1)) 
        diff_W = True
      else : 
        print("Welch's t-test:          NOT PASSED p-value={}".format(p_test1)) 
        diff_W = False 

      _, p_test2 = ks_2samp(self.A, self.B)
      if p_test2 < self.confidence:
        diff_KS = True
        print("Kolmogorov-Smirnov test:   PASSED p-value={}".format(p_test2))
      else : 
        print("Kolmogorov-Smirnov test: NOT PASSED p-value={}".format(p_test2))
        diff_KS = False 
      
      print('='*self.n + '='*len(self.string) + '='*self.n)
      if np.sum([diff_S,diff_W,diff_KS])>=2 :
        print('A and B are significantly different with {}% confidence'.format((1-self.confidence)*100)) 
        return True
      else :
        print('A and B are NOT significantly different with {}% confidence'.format((1-self.confidence)*100))
        return False 
    else : 
      print('Error: distributions are not normal - more measurements are required')
      return False

if __name__=="__main__":


    a = [30.02,29.99,30.11,29.97,30.01,29.99]
    b = [29.89,29.93,29.72,29.98,30.02,29.98]
    aa = comparator(A=a,B=b,normaltest=False)
    bb = aa.compare()
    aa.plot(bins=100)
    print(bb)