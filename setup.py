from setuptools import setup, find_packages

setup(
   name='stat_analysis',
   version='1.0.1',
   description='scientific stat tools',
   author='David Preti',
   license = "MIT",
   author_email='preti.david@gmail.com',
   url = "https://github.com/pretidav/stat_analysis",
   packages=find_packages(include=['stat_analysis', 'stat_analysis.*']),  
   install_requires=['matplotlib==3.3.3',
                     'numpy==1.18.5',
                     'scipy==1.3.1']
)