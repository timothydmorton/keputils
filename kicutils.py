import pandas as pd
import numpy as np
import os

import distributions as dists

STELLARFILE = 'keplerstellar.csv'

DATA = pd.read_csv(STELLARFILE)
DATA.index = DATA.kepid

def get_property(kic,*args):
    return DATA.ix[kic,list(args)]


