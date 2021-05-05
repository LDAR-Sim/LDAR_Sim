"""[summary]
    """
import scipy
import numpy as np


def fit_dist(samples=None, fit_params=None, dist_type="lognorm", floc=0,  mu=None, sigma=None):
    dist = getattr(scipy.stats, dist_type)
    if samples is not None:
        # Lognormal cannot have 0 values
        if dist_type == "lognorm":
            samples = [s for s in samples if s > 0]
        param = dist.fit(samples, floc=floc)
        loc = param[-2],
        scale = param[-1]
        shape = param[:-2]
    elif fit_params is not None:
        loc = fit_params[-2],
        scale = fit_params[-1]
        shape = fit_params[:-2]
    elif mu and dist_type == "lognorm":
        loc = 0
        scale = np.exp(mu)
        shape = [sigma]
    return dist(*shape, loc=loc, scale=scale)


def dist_rvs(distribution, max_size=None, gpsec_conversion=None):
    while True:
        leaksize = distribution.rvs()  # Get Random Value from Distribution
        if gpsec_conversion:
            leaksize * gpsec_conversion  # Convert to g/s
        if leaksize < max_size:
            break  # Rerun if value is larger than maximum
        else:
            x = 10
    return leaksize
