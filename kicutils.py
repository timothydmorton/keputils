"""
Convenient access to Kepler stellar table

"""

from __future__ import division,print_function
import pandas as pd
import numpy as np
import os,os.path

import distributions as dists

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

def get_property(kic,*args):
    return DATA.ix[kic,list(args)]


