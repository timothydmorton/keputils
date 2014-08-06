"""
A module for convenient access to Kepler stellar table

"""

from __future__ import division,print_function
import pandas as pd
import numpy as np
import os,os.path

from .errors import MissingDatafileError
from . import koiutils as ku

STELLARFILE = os.path.expanduser('~/.keputils/keplerstellar.csv')
H5FILE = os.path.expanduser('~/.keputils/keptables.h5')

if not os.path.exists(STELLARFILE):
    raise MissingDatafileError('Kepler stellar data file not in proper location')

def _write_hdf():
    """Loads stellar data from .csv file and then rewrites to .h5 file

    Should automaticall run just once the first time the module is imported.
    """
    print('loading stellar data from .csv file (should just happen once)')
    DATA = pd.read_csv(STELLARFILE)
    DATA.index = DATA.kepid
    DATA = DATA[~np.isnan(DATA['mass'])]
    DATA.to_hdf(H5FILE,'keplerstellar')

try:
    DATA = pd.read_hdf(H5FILE,'keplerstellar')
except:
    _write_hdf()
    DATA = pd.read_hdf(H5FILE,'keplerstellar')

def get_property(name,*args):
    """Convenience function to quickly retrieve any stellar property/properties for a given KepID/KOI numbers

    Parameters
    ----------
    name : int, float or str, or array_like
           KOI or KIC name (or array of names)
    *args : string,
            properties to return (must be valid column names of stellar properties table)

    Returns
    -------
    Selected information 
    
    """

    #First, attempt to treat name as a KOI identifier
    try:
        if len(args)==1:
            return DATA.ix[ku.DATA[name]['kepid'],args]
        else:
            return DATA.ix[ku.DATA[name]['kepid'],list(args)]

    #Otherwise, assume that it's a KIC number
    except KeyError:
        if len(args)==1:
            return DATA.ix[name,args]
        else:
            return DATA.ix[name,list(args)]


