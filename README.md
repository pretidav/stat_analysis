![](https://github.com/pretidav/stat_analysis/actions/workflows/python-app.yml/badge.svg)
[![codecov](https://codecov.io/gh/pretidav/stat_analysis/branch/main/graph/badge.svg)](https://codecov.io/gh/pretidav/stat_analysis)

# stat_analysis:
This repository contains several statistical tools useful for scientific computations. 

## pfit
Is an linear (in the parameters) fitting script which takes into account statistical uncertainties on y-axis. Chi^2 is used a likelihood function, minimized analytically. 

Once requirements are installed with 

~~~
pip install requirements
~~~

For unit testing the code can be executed as 
~~~
python pfit.py 
~~~

Import the module as 
~~~
from stat_analysis.pfit import pfit
~~~

For common usage, class _pfit_ can be customized with the following arguments:

~~~
x          # input data in list or np.array format 
y          # input data in list or np.array format
dy         # [Optional] input data in list or np.array format, if missing error is ignored (i.e. =1)
ndeg=1     # degree of polynomial, i.e. 0 is a constant fit, 1 is a*x+b and so on.
kconst=[2] # [Optional] a list of coefficients, starting from the highest to the lowest degree. (e.g. ndeg=3, kconst=[2,3] is a*x**3+b*x**2+2*x+3) these coefficients are kept fix in the fit. 
~~~

* .log(): fit parameters with uncertainties, reduced chi2, and covariance matrix are displayed. 
~~~
==================== Fit Log ====================
 k       = [4.98881479 1.89398851 6.6610509 ]
dk       = [ 1.25188083  9.53787807 10.14975134]
t        = [3.98505565 0.19857546 0.65627725]
p-values = [0.00528968 0.84823908 0.53261758]
chi2/dof = 0.0007074425784127696
dof      = 7
cov      = 
[[  1.56720562 -11.82348128  11.5408929 ]
 [-11.82348128  90.971118   -91.18678554]
 [ 11.5408929  -91.18678554 103.01745234]]
pred   = 631.1415143152262
dpred  = 58.04015781775017
~~~

* .plot(): plot the data and fit with error band. Optional parameters are xlabel,ylabel and savefile. if nor specified the plot will not be saved. 

![alt text](https://github.com/pretidav/stat_analysis/raw/main/fig/quad.png)

* .predict(): plot the data and fit with error band and the predicted point x. Optional parameters are xlabel,ylabel and savefile. if not specified the plot will not be saved. 

![alt text](https://github.com/pretidav/stat_analysis/raw/main/fig/quad_pred.png)

## example usage:
~~~ 
x = np.linspace(0,10,num=10)
y = 5*x**2+ 2*x + 5 + 2*np.random.rand(len(x))
dy = 100*np.random.rand(len(x))

ff = pfit(x=x,y=y,dy=dy,ndeg=2)
ff.fit()
ff.plot(xlabel='x',ylabel='y',savefile='../fig/quad.png')
plt.clf()
ff.predict(x=11,xlabel='x',ylabel='y',savefile='../fig/quad_pred.png')
ff.log()
~~~

# nlfit

This routine allows to perform non-linear fits with errors on both axis. If errors are not provided they are ignored. 
Input function has to be passed in this form (for instance): 

Once requirements are installed with
~~~
pip install requirements
~~~

For unit testing the code can be executed as

~~~
python nlfit.py 
~~~

Import the module as
~~~
from stat_analysis.nlfit import nlfit
~~~

For common usage, class _pfit_ can be customized with the following arguments:
~~~
f  # input function to be fitted (see below) 
x  # input data in list or np.array format
y  # input data in list or np.array format
dx # [Optional] input data in list or np.array format
dy # [Optional] input data in list or np.array format
k0 # parameters initial values for the optimizer e.g. [0.,0., ... ]. Notice that the length of this vector *must* match the number of parameter of f function.  
~~~

The input function f should be of this form: 
~~~
import numpy as np
    def f(B, x):
        return np.exp(B[0]*x) + B[1]*np.sin(x) + B[2] 
~~~


* .log(): fit parameters with uncertainties, R^2, and covariance matrix are displayed. 
~~~
==================== Fit Log ====================
 k       = [0.20230562 0.91546002 5.48977518]
dk       = [0.0030456  0.06418912 0.06665966]
t        = [66.42561823 14.26191952 82.35528149]
p-values = [0.00000000e+00 6.87618851e-11 0.00000000e+00]
R**2     = 5.540221043876636
dof      = 17
cov      = 
[[ 9.27565727e-06 -4.12808332e-05 -1.41792933e-04]
 [-4.12808332e-05  4.12024270e-03 -6.44158588e-05]
 [-1.41792933e-04 -6.44158588e-05  4.44351047e-03]]
 k       = [13.05072629]
dk       = [0.24797352]
=================================================
~~~
* .plot(): plot the data and fit with error band. Optional parameters are xlabel,ylabel and savefile. if nor specified the plot will not be saved. 

![alt text](https://github.com/pretidav/stat_analysis/raw/main/fig/nonlin.png)

* .predict():  plot the data and fit with error band and the predicted point x. Optional parameters are xlabel,ylabel and savefile. if not specified the plot will not be saved. 

![alt text](https://github.com/pretidav/stat_analysis/raw/main/fig/nonlin_pred.png)
## example usage: 
~~~
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
~~~

# bootstrap 
This routine allows for two kind of bootstrap resampling methods. 

* bootstrap: usual bootstrap with repetition with possibility of data blocking. 
* synt_bootstrap: syntetic bootstrap data generated stating from a vector of parameters with a given covariance. 

The modules can be imported as 
~~~
from stat_analysis.bootstrap import bootstrap
BS=bootstrap(k=data,Nb=10000000)
b=BS.sample()
print(np.mean(b,axis=0))
print(np.std(b,axis=0))
~~~
or 
~~~
from stat_analysis.bootstrap import synt_bootstrap

k = [2,3]
cov = [[0.3,0.5],[0.5,2]]
BS=synt_bootstrap(k=k,Nb=10000000,cov=cov)
b=BS.sample()
print(np.cov(b.T))
print(np.mean(b,axis=0))
~~~


# comparator
This routine allows for the comparison of two arrays of data. A pipeline of statistical tests, including Welch's t-test, Student's t-test and Kolmogorov-Smirnov test are included to distinguish with a given confidence if the data are coming from the same distribution or not. 

~~~
from stat_analysis.comparator import comparator
a = [30.02,29.99,30.11,29.97,30.01,29.99]
b = [29.89,29.93,29.72,29.98,30.02,29.98]
aa = comparator(A=a,B=b,normaltest=False)
bb = aa.compare()
aa.plot(bins=100)
print(bb)
~~~
