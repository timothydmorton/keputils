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

    Returns
    -------
    dist : `DoubleGauss_Distribution` for the given property

    """
    val,u1,u2 = kicu.get_property(name,[prop,
                                        '{}_err1'.format(prop), #upper error bar (positive)
                                        '{}_err2'.format(prop2)]) #lower error bar (negative)
    return dists.fit_doublegauss(val,-u2,u1)

def smass_distribution(name,default_unc=0.1):
    """Stellar mass probability distribution for given Kepler target star

    Parameters
    ----------
    name : string, int, or float
        KIC number, or any reasonable KOI identifier.

    default_unc : float
        Fractional uncertainty to use in the case that the
        catalog does not have uncertainty.  Default = 0.1.

    Returns
    -------
    dist : `DoubleGauss_Distribution` of stellar mass, using the
        values and errors provided by the Kepler stellar catalog,
        treating them as median & 68.3% confidence interval.
    """
    dist = get_distribution(name,'mass')
    dist.name = 'M'
    if np.isnan(dist.siglo):
        dist.siglo = dist.mu*default_unc
    if np.isnan(dist.sighi):
        dist.sighi = dist.mu*default_unc
    return dist

def srad_distribution(name,default_unc=0.1):
    """Stellar radius probability distribution for given Kepler target star

    Parameters
    ----------
    name : string, int, or float
        KIC number, or any reasonable KOI identifier.

    default_unc : float
        Fractional uncertainty to use in the case that the
        catalog does not have uncertainty.  Default = 0.1.

    Returns
    -------
    dist : `DoubleGauss_Distribution` of stellar radius, using the
        values and errors provided by the Kepler stellar catalog,
        treating them as median & 68.3% confidence interval.
    """

    dist = get_distribution(name,'radius')
    dist.name = 'R'
    if np.isnan(dist.siglo):
        dist.siglo = dist.mu*default_unc
    if np.isnan(dist.sighi):
        dist.sighi = dist.mu*default_unc
    return dist

def feh_distribution(name,default_unc=0.2):
    """Stellar mass probability distribution for given Kepler target star

    Parameters
    ----------
    name : string, int, or float
        KIC number, or any reasonable KOI identifier.

    default_unc : float
        Absolute uncertainty to use in the case that the
        catalog does not have uncertainty.  Default = 0.2.

    Returns
    -------
    dist : `DoubleGauss_Distribution` of stellar [Fe/H], using the
        values and errors provided by the Kepler stellar catalog,
        treating them as median & 68.3% confidence interval.
    """
    dist = get_distribution(name,'feh')
    dist.name = '[Fe/H]'
    if np.isnan(dist.siglo):
        dist.siglo = default_unc
    if np.isnan(dist.sighi):
        dist.sighi = default_unc
    return dist
