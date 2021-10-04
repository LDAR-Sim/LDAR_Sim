from math import ceil, floor
from numpy.random import choice
from numpy import average


def est_n_crews(m, sites):
    m_name = m['label']
    avg_sites_per_day = est_site_p_day(m, sites)
    try:
        avg_days_per_campaign = ceil(average([365 / s['{}_RS'.format(m_name)] for s in sites]))
        n_crews = ceil(len(sites)/(avg_sites_per_day*avg_days_per_campaign))
    except KeyError:
        n_crews = 1
    return n_crews


def est_site_p_day(m, sites):
    def s_per_day(s):
        # Calc sites per day based on single site parameters
        workday_aj = work_mins - int(choice(m['t_bw_sites']['vals']))
        t_per_site = int(choice(m['t_bw_sites']['vals'])) + int(s['{}_time'.format(m_name)])
        return workday_aj / t_per_site
    m_name = m['label']
    work_mins = m['max_workday']*60
    try:
        est_val = floor(average([s_per_day(s) for s in sites]))
    except KeyError:
        est_val = 1
    return est_val
