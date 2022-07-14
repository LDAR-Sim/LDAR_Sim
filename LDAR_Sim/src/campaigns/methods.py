from random import sample
from math import floor, ceil
from numpy import zeros, ones, tile, array


def setup_campaigns(campaigns, prog_params, n_sites, n_screening_rs_sets):
    """ Setup Campaigns

    Args:
        campaigns (Class.state): Campaign Object
        prog_params (_type_): _description_
        n_sites (_type_): _description_
        n_screening_rs_sets (_type_): _description_
    """
    for midx, rs in n_screening_rs_sets.items():
        meth = prog_params['methods'][midx]
        if rs != "varies" or meth['follow_up']['min_followup_type'] == 'annual':
            if meth['follow_up']['min_followup_type'] == 'campaign':
                days_in_campaign = int(floor(365/rs))
            else:
                days_in_campaign = 365
            n_campaigns = int(ceil(prog_params['timesteps']/days_in_campaign)+1)
            min_followups = meth['follow_up']['min_followups']
            min_FU_d_to_end = meth['follow_up'][
                'min_followup_days_to_end']
            if len(min_followups) == 0:
                # Visit all sites
                min_followups_sites = zeros(n_campaigns)
            elif len(min_followups) == 1:
                # apply value to all campaigns
                min_followups_sites = ones(n_campaigns)*min_followups[0]*n_sites
            else:
                reps = int(ceil(n_campaigns/len(min_followups)))
                min_followups_sites = tile(array(min_followups) * n_sites, reps)

            campaigns.update(
                {midx:
                    {
                        'n_days': days_in_campaign,
                        'min_followups': min_followups_sites,
                        'n_campaigns': n_campaigns,
                        'current_campaign': 0,
                        'schedule': [cnt*days_in_campaign
                                     for cnt in range(n_campaigns)],
                        'min_FU_check': min_FU_d_to_end,
                        'FU_check_ts': days_in_campaign-min_FU_d_to_end,
                        'sites_followed_up': set([])
                    }
                 })


def update_campaigns(campaigns, sites, cur_ts, current_date):
    for midx, cpgn in campaigns.items():
        next_camp_start = cpgn['schedule'][cpgn['current_campaign']+1]
        if cpgn['current_campaign'] < cpgn['n_campaigns'] \
                and cur_ts > next_camp_start:
            # Move to next Campaign
            campaigns[midx].update({
                'sites_followed_up': set([]),
                'current_campaign': cpgn['current_campaign']+1,
                'FU_check_ts': next_camp_start + (
                    cpgn['n_days'] - cpgn['min_FU_check']
                ),
            })
        if cur_ts == cpgn['FU_check_ts']:
            # Move flag sites
            FU_sites = [s for s in sites
                        if s['facility_ID'] in cpgn['sites_followed_up']]
            Non_FU_sites = [s for s in sites
                            if s['facility_ID'] not in cpgn['sites_followed_up']]
            makeup_cnt = cpgn['min_followups'][cpgn['current_campaign']] - len(FU_sites)
            if makeup_cnt < 0:
                makeup_cnt = 0
            flag_sites = sample(Non_FU_sites, int(makeup_cnt))
            for site in flag_sites:
                site['currently_flagged'] = True
                site['date_flagged'] = current_date
                site['flagged_by'] = 'makeup'
