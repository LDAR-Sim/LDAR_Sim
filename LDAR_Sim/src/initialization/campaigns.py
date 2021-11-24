
from math import floor
from numpy import zeros
# --- initialize Campaigns ---


def _add_method_campaign(campaign_s_t, d_per_campaign, timesteps, n_sites, m_name):
    n_campaigns = floor(timesteps/d_per_campaign)
    return campaign_s_t.update(
        {
            m_name: {
                'current_campaign': 0,
                'n_campaigns': n_campaigns,
                'ts_start': [c*d_per_campaign for c in range(0, n_campaigns)],
                'n_sites': n_sites,
                'n_sites_screened': zeros(n_campaigns, dtype=int),
                'n_sites_surveyed': zeros(n_campaigns, dtype=int),
                'n_flags': zeros(n_campaigns, dtype=int),
                'n_tags': zeros(n_campaigns, dtype=int),
                'n_repairs': zeros(n_campaigns, dtype=int)
            }
        })


def init_campaigns(n_subtype_rs, sites_per_subtype, timesteps):
    """ Initialize campaigns by going through all site subtypes, and all
        methods, and setting up campaign periods for each. IF subtypes have
        one or more scheduled method with a single rs value, all unscheduled
        methods ie. OGI_FU and natural will have the same schedule.

    Args:
        n_subtype_rs (dict): dict of dicts where key is subtype and val is a dict with
                             key as method and val of the RS associated with the method/subtype.
                             If no single RS value for subtype set to None.
                             If method is un-scheduled (OGI-FU or Natural) set to -1.
        sites_per_subtype (dict): dict where key is subtype and val is number of sites in
                             in subtype.
        timesteps (integer): [description]

    Returns:
        dict: campaign object. Where campaign['subtype_code]['method'] = {
                            'current_campaign': 0,
                            'n_campaigns': n_campaigns,
                            'ts_start': [c*d_per_campaign for c in range(0, n_campaigns)],
                            'n_sites': n_sites,
                            'n_sites_screened': zeros(n_campaigns, dtype=int),
                            'n_sites_surveyed': zeros(n_campaigns, dtype=int),
                            'n_flags': zeros(n_campaigns, dtype=int),
                            'n_tags': zeros(n_campaigns, dtype=int),
                            'n_repairs': zeros(n_campaigns, dtype=int)
                            }
    """
    campaigns = {}
    for s_t, s_vals in n_subtype_rs.items():
        ref_day_per_campaign = None
        has_one_campaign = True
        campaigns.update({s_t: {}})
        non_sched_meths = []
        for m_idx, m_rs in s_vals.items():
            if m_rs != -1:
                if m_rs is not None:
                    d_per_campaign = int(floor(365/m_rs))
                    if has_one_campaign is True:
                        if ref_day_per_campaign is None:
                            ref_day_per_campaign = d_per_campaign
                        elif ref_day_per_campaign != d_per_campaign:
                            has_one_campaign = False
                else:
                    # If campaign lengths are not set or vary, set the n of campaigns to annual
                    has_one_campaign = False
                    d_per_campaign = 365
                _add_method_campaign(campaigns[s_t], d_per_campaign, timesteps,
                                     sites_per_subtype[s_t], m_idx)
            else:
                non_sched_meths.append(m_idx)

        # Add non-scheduled methods
        # if there is a only one RS value for all sites and methods is subtype then
        # set non-scheduled methods to havethe asame survey period
        for m in non_sched_meths:
            if has_one_campaign and ref_day_per_campaign is not None:
                d_per_campaign = ref_day_per_campaign
            else:
                d_per_campaign = 365
            _add_method_campaign(campaigns[s_t], d_per_campaign, timesteps,
                                 sites_per_subtype[s_t], m)

    return campaigns
