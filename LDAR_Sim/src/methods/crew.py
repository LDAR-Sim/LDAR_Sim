# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.crew
# Purpose:     initialize crew, work_a_day, visit sites, and detect_emissions
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

# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------

from datetime import timedelta
from importlib import import_module

import numpy as np


class BaseCrew:
    """ Base crws are used by methods to generate crew-level deployment and scheduling,
        determine sites ready for survey, alocate sites to crews, and report on emissions.
        Crew method consists of a deployment type and a sensor type which are set using
        the input parameter file.
    """

    def __init__(self, state, parameters, config, timeseries, deployment_days, id, site=None):
        """
        Constructs an individual crew based on defined configuration.
        """
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.deployment_days = deployment_days
        self.itinerary = None
        self.id = id
        self.site = site  # Used by stationary deployment methods
        if len(config['scheduling']['LDAR_crew_init_location']) > 0:
            self.lat = float(config['scheduling']
                             ['LDAR_crew_init_location'][1])
            self.lon = float(config['scheduling']
                             ['LDAR_crew_init_location'][0])
        else:
            self.lat = 0
            self.lon = 0
        sched_mod = import_module('methods.deployment.{}_crew'.format(
            self.config['deployment_type'].lower()))
        # Get schedule based on deployment type
        Schedule = getattr(sched_mod, 'Schedule')
        self.schedule = Schedule(self.id, self.lat, self.lon, state,
                                 config, parameters,  deployment_days)

        if self.config['deployment_type'] == 'mobile':
            self.worked_today = False
            self.rollover_site = None
            self.scheduling = self.config['scheduling']

        return

    def work_a_day(self, site_pool, candidate_flags=None):
        """
        Go to work and find the leaks for a given day
        """
        m_name = self.config['label']
        self.worked_today = False
        self.candidate_flags = candidate_flags
        self.days_skipped = 0
        self.daily_cost = 0
        daily_LDAR_time = 0
        daily_travel_time = 0
        # If there are sites ready for survey
        if len(site_pool) > 0:
            itinerary = self.schedule.start_day(site_pool)
            for site_plan in itinerary:
                if site_plan['remaining_mins'] == 0:
                    # Only record and fix leaks on the last day of work if theres rollover
                    self.visit_site(site_plan['site'])
                self.worked_today = True
                # NOTE Mobile LDAR_mins also includes travel to site time
                self.state['t'].current_date += timedelta(minutes=int(site_plan['LDAR_mins']))
                self.daily_cost += self.config['cost']['per_site']
                if self.config['deployment_type'] == 'mobile':
                    daily_LDAR_time += site_plan['LDAR_mins_onsite']
                    daily_travel_time += site_plan['travel_to_mins']

        # Update time series and variables and run end day if crew works
        if self.worked_today:
            cur_timestep = self.state['t'].current_timestep
            self.schedule.end_day(site_pool, itinerary)
            # n_hours =
            self.daily_cost += self.config['cost']['per_hour'] * \
                (self.state['t'].current_date.hour-self.schedule.start_hour)
            self.daily_cost += self.config['cost']['per_day']
            self.timeseries['{}_cost'.format(m_name)][cur_timestep] += self.daily_cost
            self.timeseries['total_daily_cost'][cur_timestep] += self.daily_cost
            self.timeseries['{}_survey_time'.format(m_name)][cur_timestep] += daily_LDAR_time
            if self.config['deployment_type'] == 'mobile':
                self.timeseries['{}_travel_time'.format(m_name)][cur_timestep] += \
                    daily_travel_time + itinerary[-1]['travel_home_mins']

    def visit_site(self, site):
        """
        Look for emissions at the chosen site.
        """
        m_name = self.config['label']
        cur_ts = self.state['t'].current_timestep
        site_detect_results = self.detect_emissions(site)

        if self.config['measurement_scale'].lower() == 'component':
            # Remove site from flag pool if component level measurement
            site.update({'currently_flagged': False})
            site['last_component_survey'] = cur_ts
            if site_detect_results['found_leak']:
                self.timeseries['{}_sites_vis_w_leaks'.format(m_name)][cur_ts] += 1
        elif site_detect_results['found_leak']:
            # all other sites flag
            self.timeseries['{}_sites_vis_w_leaks'.format(m_name)][cur_ts] += 1
            self.candidate_flags.append(site_detect_results)

        # Update site
        self.timeseries['{}_sites_visited'.format(m_name)][cur_ts] += 1
        site['{}_surveys_conducted'.format(m_name)] += 1
        site['{}_surveys_done_this_year'.format(m_name)] += 1
        site['historic_t_since_LDAR'] = site['{}_t_since_last_LDAR'.format(m_name)]
        site['{}_t_since_last_LDAR'.format(m_name)] = 0

    def detect_emissions(self, site, *args):
        """ Run module to detect leaks and tag sites
        Returns:
            dict: {
                'site': site,
                '*args':  Various sensor parameters, see user manual for more info.
            }
        """
        m_name = self.config['label']
        covered_leaks = []
        is_sp_covered = True
        covered_site_rate = 0
        site_rate = 0
        covered_equipment_rates = [0] * int(site['equipment_groups'])
        equipment_rates = [0] * int(site['equipment_groups'])
        for leak in site['active_leaks']:
            # Check to see if leak is spatially covered
            if '{}_sp_covered'.format(m_name) not in leak:
                is_sp_covered = np.random.binomial(1, self.config['coverage']['spatial'])
                leak['{}_sp_covered'.format(m_name)] = is_sp_covered
            if leak['{}_sp_covered'.format(m_name)]:
                # Check to see if leak is temporally covered
                if np.random.binomial(1, self.config['coverage']['temporal']):
                    covered_leaks.append(leak)
                    covered_site_rate += leak['rate']
                    covered_equipment_rates[leak['equipment_group']-1] += leak['rate']
            site_rate += leak['rate']
            equipment_rates[leak['equipment_group']-1] += leak['rate']
            # Get the type of sensor, and call the the detect emissions function for sensor
            # Aggregate true emissions to equipment and site level; get list of leaks present

        # Add vented emissions
        venting = 0
        if self.parameters['emissions']['consider_venting']:
            venting = self.state['empirical_vents'][
                np.random.randint(0, len(self.state['empirical_vents']))]
            covered_site_rate += venting
            site_rate += venting
            for rate in range(len(covered_equipment_rates)):
                covered_equipment_rates[rate] += venting/int(site['equipment_groups'])
                equipment_rates[rate] += venting/int(site['equipment_groups'])
        # Import module. If none is specified use method.sensors.{method_type}
        if self.config['sensor']['mod_loc'] is None:
            sensor_mod = import_module(
                'methods.sensors.{}'.format(self.config['sensor']['type']))
        else:
            sensor_mod = import_module(self.config['sensor']['mod_loc'])
        detect_emis_sensor = getattr(sensor_mod, 'detect_emissions')
        return detect_emis_sensor(self, site, covered_leaks, covered_equipment_rates,
                                  covered_site_rate, site_rate, venting, equipment_rates)
