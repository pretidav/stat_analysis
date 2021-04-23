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

For common usage, class _pfit_ can be customized with the following arguments:

~~~
x          # input data in list or np.array format 
y          # input data in list or np.array format
dy         # [Optional] input data in list or np.array format, if missing error is ignored (i.e. =1)
ndeg=1     # degree of polynomial, i.e. 0 is a constant fit, 1 is a*x+b and so on.
kconst=[2] # [Optional] a list of coefficients, starting from the highest to the lowest degree. (e.g. ndeg=3, kconst=[2,3] is a*x**3+b*x**2+2*x+3) these coefficients are kept fix in the fit. 
~~~

* .log(): fit parameters with uncertainties, reduced chi2, and covariance matrix are displayed. 

* .plot(): plot the data and fit with error band. Optional parameters are xlabel,ylabel and savefile. if nor specified the plot will not be saved. 

![alt text](https://github.com/pretidav/stat_analysis/raw/main/fig/quad.png)


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
    def f(B, x):
        return np.exp(B[0]*x) + B[1]*np.sin(x) + B[2] 
~~~


* .log(): fit parameters with uncertainties, R^2, and covariance matrix are displayed. 

* .plot(): plot the data and fit with error band. Optional parameters are xlabel,ylabel and savefile. if nor specified the plot will not be saved. 

![alt text](https://github.com/pretidav/stat_analysis/raw/main/fig/nonlin.png)

# bootstrap 
This routine allows for two kind of bootstrap resampling methods. 

* bootstrap: usual bootstrap with repetition with possibility of data blocking. 
* synt_bootstrap: syntetic bootstrap data generated stating from a vector of parameters with a given covariance. 
# comparator
This routine allows for the comparison of two arrays of data. A pipeline of statistical tests, including Welch's t-test, Student's t-test and Kolmogorov-Smirnov test are included to distinguish with a given confidence if the data are coming from the same distribution or not. 