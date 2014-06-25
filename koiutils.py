"""
Module for convenient access to kepler table data.


"""
from __future__ import division,print_function
import numpy as np
import os,sys,re,os.path

import pandas as pd

from .errors import MissingDatafileError,BadKOINameError

def koiname(k, star=False, koinum=False):
    """Returns KOI name in standard format.

    if star is False, K?????.??; otherwise K?????

    if koinum is True, the returns number rather than string, no K.
    """
    name = ''
    if type(k) in (type(1),np.int64):
        name = 'K%08.2f' % (k+0.01)
    elif type(k) in (type(1.),np.float64,np.float32):
        name = 'K%08.2f' % k
    else:
        if type(k) == type(''):
            k = k.strip()
        m = re.search('^(\d+)$',k)
        if m:
            name = 'K%08.2f' % (int(m.group(1)) + 0.01)
        m = re.search('^(\d+\.\d+)$',k)
        if m:
            name = 'K%08.2f' % (float(m.group(1)))
        m = re.search('(K\d\d\d\d\d[A-Z]?$)',k)
        if m:
            name = '%s.01' % m.group(1)
        m = re.search('(K\d\d\d\d\d\.\d\d)',k)
        if m:
            name = '%s' % m.group(1)
        m = re.search('[Kk][Oo][Ii][-_]?(\d+)$',k)
        if m:
            name = 'K%05i.01' % int(m.group(1))
        m = re.search('[Kk][Oo][Ii][-_]?((\d+)\.(\d+))',k)
        if m:
            name = 'K%08.2f' % float(m.group(1))
        if name == '':
            raise KeyError('"%s" not a valid KOI name' % k)
    if star:
        name = name[:-3]
        if koinum:
            m = re.search('K(\d\d\d\d\d)',name)
            name = int(m.group(1))
    else:
        if koinum:
            m = re.search('K(\d\d\d\d\d\.\d\d)',name)
            name = float(m.group(1))
    return name
    
def koistarnum(k):
    return koiname(k,star=True,koinum=True)

def koistar(k):
    return koiname(k,star=True)

class KOI_DataFrame(pd.DataFrame):
    """A subclass of a pandas DataFrame that allows "sloppy" access to kois.

    e.g. DATA[5] or DATA[5.01] or DATA['KOI5'], DATA['KOI-5'], etc. 
        are all equivalent to DATA.ix['K00005.01']
    """

    def __getitem__(self,item):
        try:
            return super(KOI_DataFrame,self).ix[koiname(item)]
        except KeyError:
            try:
                return super(KOI_DataFrame,self).ix[koiname(item,koinum=True)]
            except KeyError:
                try:
                    return super(KOI_DataFrame,self).ix[koiname(item,star=True)]
                except:
                    return super(KOI_DataFrame,self).__getitem__(item)
        except:
            return super(KOI_DataFrame,self).__getitem__(item)

KOIFILE = os.path.expanduser('~/.keputils/kois_cumulative.csv')
H5FILE = os.path.expanduser('~/.keputils/keptables.h5')

if not os.path.exists(KOIFILE):
    raise MissingDatafileError('Cumulative KOI data file not in proper location (run getdata.sh)')


def _write_hdf():
    """
    Should only run once: reads data from .csv file and writes to .h5.
    """
    
    print('loading stellar data from .csv file (should just happen once)')
    DATA = pd.read_csv(KOIFILE)
    DATA.index = DATA.kepid
    DATA.to_hdf(H5FILE,'kois_cumulative')


try:
    DATA = KOI_DataFrame(pd.read_hdf(H5FILE,'kois_cumulative'))
except:
    _write_hdf()
    DATA = KOI_DataFrame(pd.read_hdf(H5FILE,'kois_cumulative'))

oldg,oldr,oldi,oldz = (DATA['koi_gmag'].copy(),
                       DATA['koi_rmag'].copy(),
                       DATA['koi_imag'].copy(),
                       DATA['koi_zmag'].copy())
newg = oldg + 0.0921*(oldg - oldr) - 0.0985
newr = oldr + 0.0548*(oldr - oldi) - 0.0383
newi = oldi + 0.0696*(oldr - oldi) - 0.0583
newz = oldz + 0.1587*(oldi - oldz) - 0.0597

DATA['koi_gmag'] = newg
DATA['koi_rmag'] = newr
DATA['koi_imag'] = newi
DATA['koi_zmag'] = newz
DATA['koi_gmag_orig'] = oldg
DATA['koi_rmag_orig'] = oldr
DATA['koi_imag_orig'] = oldi
DATA['koi_zmag_orig'] = oldz

def radec(koi):
    """
    Returns the ra and dec of a given KOI.

    Parameters
    ----------
    koi : str, int, or float
          KOI name

    Returns
    -------
    ra,dec : float [decimal degrees]
    """
    
    return DATA[koi]['ra'],DATA[koi]['dec']

def KICmags(koi,bands=['g','r','i','z','j','h','k','kep']):
    """
    Returns the apparent magnitudes of given koi in given bands

    Parameters
    ----------

    
    """
    mags = {b:DATA[koi]['koi_%smag' % b] for b in bands}
    mags['J'] = mags['j']
    mags['Ks'] = mags['k']
    mags['K'] = mags['k']
    mags['H'] = mags['h']
    mags['Kepler'] = mags['kep']
    return mags

def KICmag(koi,band):
    mags = KICmags(koi)
    return mags[band]



