from __future__ import division,print_function
__author__ = 'Timothy D. Morton <tim.morton@gmail.com>'
"""
Module for convenient access to kepler cumulative KOI table data.
"""
import numpy as np
import os,sys,re,os.path

import pandas as pd

try:
    from simpledist import distributions as dists
except:
    dists = None

from .errors import BadKOINameError
from .utils import koiname, koistar, koistarnum

KOIFILE = os.path.expanduser('~/.keputils/kois_cumulative.csv')
H5FILE = os.path.expanduser('~/.keputils/keptables.h5')


#### from DFM #####
import requests
from cStringIO import StringIO

def get_catalog(name, basepath=os.path.expanduser('~/.keputils')):
    fn = os.path.join(basepath, "{0}.h5".format(name))
    if os.path.exists(fn):
        return pd.read_hdf(fn, name)
    if not os.path.exists(basepath):
        os.makedirs(basepath)
    print("Downloading {0}...".format(name))
    url = ("http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/"
           "nph-nstedAPI?table={0}&select=*").format(name)
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        r.raise_for_status()
    fh = StringIO(r.content)
    df = pd.read_csv(fh)
    df.to_hdf(fn, name, format="t")
    return df

######

def _download_koitable():
    """Downloads cumulative KOI table from Exoplanet Archive and saves it to ~/.keputils
    """
    import urllib2
    if not os.path.exists(os.path.expanduser('~/.keputils')):
        os.makedirs(os.path.expanduser('~/.keputils'))
    print('Downloading cumulative KOI table and saving to ~/.keputils/kois_cumulative.csv...')
    url = 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=cumulative&select=*'
    u = urllib2.urlopen(url)
    f = open(KOIFILE,'w')
    f.write(u.read())
    f.close()

if not os.path.exists(KOIFILE):
    _download_koitable()
    
def _write_hdf():
    """
    Should only run once: reads data from .csv file and writes to .h5.
    """
    
    print('loading stellar data from .csv file (should just happen once)')
    DATA = pd.read_csv(KOIFILE)
    DATA.index = DATA['kepoi_name']
    DATA.to_hdf(H5FILE,'kois_cumulative')

def update_data():
    """Run this to get the latest cumualtive KOI table.
    """
    _download_koitable()
    _write_hdf()

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

def fix_kicmags(df):
    oldg,oldr,oldi,oldz = (df['koi_gmag'].copy(),
                           df['koi_rmag'].copy(),
                           df['koi_imag'].copy(),
                           df['koi_zmag'].copy())
    newg = oldg + 0.0921*(oldg - oldr) - 0.0985
    newr = oldr + 0.0548*(oldr - oldi) - 0.0383
    newi = oldi + 0.0696*(oldr - oldi) - 0.0583
    newz = oldz + 0.1587*(oldi - oldz) - 0.0597

    df['koi_gmag'] = newg
    df['koi_rmag'] = newr
    df['koi_imag'] = newi
    df['koi_zmag'] = newz
    df['koi_gmag_orig'] = oldg
    df['koi_rmag_orig'] = oldr
    df['koi_imag_orig'] = oldi
    df['koi_zmag_orig'] = oldz

try:
    DATA = KOI_DataFrame(pd.read_hdf(H5FILE,'kois_cumulative'))
except:
    _write_hdf()
    DATA = KOI_DataFrame(pd.read_hdf(H5FILE,'kois_cumulative'))

fix_kicmags(DATA)

DR24 = KOI_DataFrame(get_catalog('q1_q17_dr24_koi'))
DR24.index = DR24.kepoi_name
fix_kicmags(DR24)


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
    Returns the apparent magnitudes of given KOI star in given bands

    Parameters
    ----------
    koi : str, int, or float
          KOI name
    bands : band names (optional)

    Returns
    -------
    mags : dict
           Magnitudes of KOI star in provided bands
    """
    mags = {b:DATA[koi]['koi_%smag' % b] for b in bands}
    mags['J'] = mags['j']
    mags['Ks'] = mags['k']
    mags['K'] = mags['k']
    mags['H'] = mags['h']
    mags['Kepler'] = mags['kep']
    return mags

def KICmag(koi,band):
    """
    Returns the apparent magnitude of given KOI star in given band.  returns KICmags(koi)[band]
    """
    return KICmags(koi)[band]

def kepid(koi):
    return DATA.ix[koiname(koi),'kepid']

def get_property(koi,prop):
    return DATA.ix[koiname(koi),prop]

def get_ncands(koi):
    return DATA.ix[koiname(koi),'koi_count']

def get_distribution(koi, prop):
    val = DATA.ix[koi, prop]
    u1 = DATA.ix[koi, prop+'_err1'] #upper error bar (positive)
    u2 = DATA.ix[koi, prop+'_err2'] #upper error bar (negative)
    return dists.fit_doublegauss(val, -u2, u1)
