# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        utils.attribute_leaks
# Purpose:     When a leak is observed, Identify who 'found' a leak and if the leak is new
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
from initialization.emissions import FugitiveEmission
from methods.reporting.estimate import get_site_t_since_last_ldar


def tag_leak(
    leak: FugitiveEmission,
    measured_rate,
    site,
    timeseries,
    time_obj,
    company,
    crew_id=1,
    prog_params=None
):
    cur_ts = time_obj.current_timestep
    if site['currently_flagged']:
        flag_company = site['flagged_by']
        flag_date = site['date_flagged']
        leak.update_detection_records(flag_company, flag_date)
    leak.update_detection_records(company, cur_ts)
    t_since_ldar = get_site_t_since_last_ldar(site, leak.get_init_detect_company())
    new_leak = leak.tag_leak(
        measured_rate,
        cur_ts, t_since_ldar,
        company,
        crew_id,
        prog_params['methods'][company]['reporting_delay']
    )
    if new_leak:
        timeseries['{}_n_tags'.format(company)][time_obj.current_timestep] += 1
        return True
    else:
        timeseries['{}_redund_tags'.format(company)][
            time_obj.current_timestep] += 1
    return False


def flag_site(config, site, timeseries, time_obj, campaign, company, consider_venting=False):
    """ Updates the flag on a site. If a site is not flagged
        This function will flag. If it is already flagged, the
        site will be marked as either"
            redundant: if the site is already flagged
            redundant 2: if the site is not tagged but has active tagged leaks
            flag w/o venting: Would the site have been flagged without venting
    Args:
        config (dict): Method parameters
        site (dict): Site output from screening survey
        timeseries (timeseries obj): ie self.timeseries
        time_obj (current time obj): current time state. ie self.state['t']
        company (str): Company responsible for detecting leak
        consider_venting (bool): is venting enabled in method?
    """
    site_obj = site['site']
    site_true_rate = site['site_measured_rate']
    venting = site['vent_rate']
    if site_obj['currently_flagged']:
        timeseries['{}_flags_redund1'.format(
            company)][time_obj.current_timestep] += 1
    else:
        # Flag the site for follow-up
        site_obj['currently_flagged'] = True

        site_obj['preferred_FU_method'] = config['follow_up']['preferred_method']

        site_obj['date_flagged'] = time_obj.current_date
        site_obj['flagged_by'] = company
        if company in campaign:
            campaign[company]['sites_followed_up'].add(site_obj['facility_ID'])
        timeseries['{}_eff_flags'.format(
            company)][time_obj.current_timestep] += 1

        # Check to see if the site has any leaks that are active and tagged
        site_leaks: int = len(
            [lk for lk in site_obj['active_leaks'] if lk.get_tagged()])

        if site_leaks > 0:
            timeseries['{}_flags_redund2'.format(
                company)][time_obj.current_timestep] += 1

        # Would the site have been chosen without venting?
        if consider_venting:
            if (site_true_rate - venting) < config['follow_up']['thresh']:
                timeseries['{}_flag_wo_vent'.format(
                    company)][time_obj.current_timestep] += 1
