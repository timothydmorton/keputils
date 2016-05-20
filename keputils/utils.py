import numpy as np
import re

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
        m = re.search('(K\d\d\d\d\d)',k)
        if m:
            name = '{}.01'.format(m.group(1))
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
