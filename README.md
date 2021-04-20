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