from __future__ import division,print_function
__author__ = 'Timothy D. Morton <tim.morton@gmail.com>'
"""
A module for convenient access to Kepler stellar table

"""

import pandas as pd
import numpy as np
import os,os.path


from . import koiutils as ku
from .cfg import KEPUTILS

from .utils import get_catalog

STELLARFILE = os.path.join(KEPUTILS, 'keplerstellar_q17.csv')
H5FILE = os.path.join(KEPUTILS, 'keptables.h5')

DATA = get_catalog('q1_q17_dr25_stellar')
    
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

