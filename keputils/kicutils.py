from __future__ import division,print_function
__author__ = 'Timothy D. Morton <tim.morton@gmail.com>'
"""
A module for convenient access to Kepler stellar table

"""

import pandas as pd
import numpy as np
import os,os.path


from . import koiutils as ku

STELLARFILE = os.path.expanduser('~/.keputils/keplerstellar_q17.csv')
H5FILE = os.path.expanduser('~/.keputils/keptables.h5')

def _download_stellartable():
    """Downloads Kepler stellar table from Exoplanet Archive and saves it to ~/.keputils
    """
    import urllib2
    if not os.path.exists(os.path.expanduser('~/.keputils')):
        os.makedirs(os.path.expanduser('~/.keputils'))
    print('Downloading Kepler stellar table and saving to ~/.keputils/keplerstellar_q17.csv...')
    url = 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=q1_q17_dr24_stellar&select=*'
    u = urllib2.urlopen(url)
    f = open(STELLARFILE,'w')
    f.write(u.read())
    f.close()

if not os.path.exists(STELLARFILE):
    _download_stellartable()

def _write_hdf():
    """Loads stellar data from .csv file and then rewrites to .h5 file

    Should automatically run just once the first time the module is imported.
    """
    print('loading stellar data from .csv file (should just happen once)')
    DATA = pd.read_csv(STELLARFILE)
    DATA.index = DATA.kepid
    DATA = DATA[~np.isnan(DATA['mass'])]
    store = pd.HDFStore(H5FILE)
    try:
        del store['keplerstellar_q17']
    except KeyError:
        pass
    store.close()
    DATA.to_hdf(H5FILE,'keplerstellar_q17')

try:
    DATA = pd.read_hdf(H5FILE,'keplerstellar_q17')
except:
    _write_hdf()
    DATA = pd.read_hdf(H5FILE,'keplerstellar_q17')

def update_data():
    """Run this to get the latest Kepler stellar data.
    """
    _download_stellartable()
    _write_hdf()
    
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

