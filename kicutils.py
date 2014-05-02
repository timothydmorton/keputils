"""
Convenient access to Kepler stellar table

"""

from __future__ import division,print_function
import pandas as pd
import numpy as np
import os,os.path

import distributions as dists

import koiutils as ku

STELLARFILE = os.path.expanduser('~/.keputils/keplerstellar.csv')
H5FILE = os.path.expanduser('~/.keputils/keptables.h5')

def write_hdf(filename=H5FILE,csvfile=STELLARFILE):
    print('loading stellar data from .csv file (should just happen once)')
    DATA = pd.read_csv(csvfile)
    DATA.index = DATA.kepid
    DATA = DATA[~np.isnan(DATA['mass'])]
    DATA.to_hdf(filename,'keplerstellar')

try:
    DATA = pd.read_hdf(H5FILE,'keplerstellar')
except:
    write_hdf()
    DATA = pd.read_hdf(H5FILE,'keplerstellar')

def get_property(name,*args):
    try:
        if len(args)==1:
            return DATA.ix[ku.DATA[name]['kepid'],args]
        else:
            return DATA.ix[ku.DATA[name]['kepid'],list(args)]            
    except:
        if len(args)==1:
            return DATA.ix[name,args]
        else:
            return DATA.ix[name,list(args)]


