import simpledist.distributions as dists 

from . import kicutils as kicu
from . import koiutils as ku

def get_distribution(name,prop):
    """Returns Distribution for given property for KIC or KOI object.

    Parameters
    ----------
    name : string, int, or float
        KIC number, or any reasonable KOI identifier.

    prop : string
        Property for which Distribution is desired
    """
    val,u1,u2 = kicu.get_property(name,[prop,
                                        '{}_err1'.format(prop), #upper error bar (positive)
                                        '{}_err2'.format(prop2)]) #lower error bar (negative)
    return dists.fit_doublegauss(val,-u2,u1)
