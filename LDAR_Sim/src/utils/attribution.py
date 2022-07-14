# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        utils.attribute_leaks
# Purpose:     When a leak is observed, Identify who 'found' a leak and if the leak is new
#
# Copyright (C) 2018-2021  Intelligent Methane Monitoring and Management System (IM3S) Group
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.
from methods.reporting.estimate import estimate_start_date


def update_tag(
        leak, measured_rate, site, timeseries,
        time_obj, company, crew_id=1, prog_params=None):
    """ Updates the tag on a leak. If a leak is not tagged
        This funciton will tag. If it is already tagged, the
        leak will be added as a redundant tag.

    Args:
        leak (leak obj): Leak object. See initialization.leaks for details
        measured_rate (int): Rate of leak in g/s
        site (dict): site object
        timeseries (timeseries obj): ie self.timeseries
        time_obj (current time obj): current time state. ie self.state['t']
        company (str): Company responsible for detecting leak
        crew_id (int, optional): [int]. Defaults to 1. crew responsible for detecting

    Returns:
        [bool]: Is the leak new?
    """
    if leak['tagged']:
        if company == 'natural':
            # natural can still repair a tagged leak
            leak['date_tagged'] = time_obj.current_date
            leak['tagged_by_company'] = company
        elif leak['tagged_by_company'] == company:
            timeseries['{}_redund_tags'.format(company)][
                time_obj.current_timestep] += 1
        return False

    elif not leak['tagged']:
        # Add these leaks to the 'tag pool'
        leak['tagged'] = True
        leak['date_tagged'] = time_obj.current_date
        if site['currently_flagged'] and site['flagged_by'] is not None:
            leak['init_detect_by'] = site['flagged_by']
            leak['init_detect_date'] = site['date_flagged']
        else:
            leak['init_detect_by'] = company
            leak['init_detect_date'] = leak['date_tagged']
        # Only estimate start date, and rate if leak was actually tagged by LDAR
        if company != 'natural':
            leak['measured_rate'] = measured_rate
            leak['estimated_date_began'] = estimate_start_date(
                leak,
                time_obj.current_timestep,
                site,
                prog_params['methods'][company],
                prog_params['methods'][leak['init_detect_by']],
            )
            leak['measured_rate'] = measured_rate

        leak['tagged_by_company'] = company
        leak['tagged_by_crew'] = crew_id
        timeseries['{}_n_tags'.format(company)][time_obj.current_timestep] += 1
        # if initially flagged give credit to flagging company
        if site['currently_flagged'] and site['flagged_by'] is not None:
            leak['init_detect_by'] = site['flagged_by']
            leak['init_detect_date'] = site['date_flagged']
        else:
            leak['init_detect_by'] = company
            leak['init_detect_date'] = leak['date_tagged']
    return True


def update_flag(config, site, timeseries, time_obj, campaign, company, consider_venting=False):
    """ Updates the flag on a site. If a site is not flagged
        This funciton will flag. If it is already flagged, the
        site will be marked as either"
            redundant: if the site is already flagged
            redundant 2: if The site is not tagged by is not site has active tagged leaks
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
        timeseries['{}_flags_redund1'.format(company)][time_obj.current_timestep] += 1
    else:
        # Flag the site for follow-up
        site_obj['currently_flagged'] = True
        site_obj['date_flagged'] = time_obj.current_date
        site_obj['flagged_by'] = company
        if company in campaign:
            campaign[company]['sites_followed_up'].add(site_obj['facility_ID'])
        timeseries['{}_eff_flags'.format(company)][time_obj.current_timestep] += 1

        # Check to see if the site has any leaks that are active and tagged
        site_leaks = len([lk for lk in site_obj['active_leaks'] if lk['tagged']])

        if site_leaks > 0:
            timeseries['{}_flags_redund2'.format(company)][time_obj.current_timestep] += 1

        # Would the site have been chosen without venting?
        if consider_venting:
            if (site_true_rate - venting) < config['follow_up']['thresh']:
                timeseries['{}_flag_wo_vent'.format(company)][time_obj.current_timestep] += 1
