# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.crew
# Purpose:     initialize crew, work_a_day, visit sites, and detect_emissions
#
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

import random
from datetime import timedelta
from importlib import import_module
from typing import Any, Dict

import numpy as np

from config.output_flag_mapping import OUTPUTS, SITE_VISITS
from initialization.emissions import FugitiveEmission


class BaseCrew:
    """ Base crews are used by methods to generate crew-level deployment and scheduling,
        determine sites ready for survey, allocate sites to crews, and report on emissions.
        Crew method consists of a deployment type and a sensor type which are set using
        the input parameter file.
    """

    def __init__(
            self,
            state,
            program_parameters,
            virtual_world,
            simulation_settings,
            config,
            timeseries,
            deployment_days,
            id,
            site=None
    ):
        """
        Constructs an individual crew based on defined configuration.
        """
        self.state = state
        self.consider_venting = virtual_world['emissions']['consider_venting']
        self.program_parameters = program_parameters
        self.simulation_settings = simulation_settings
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
        self.schedule = Schedule(
            self.id,
            self.lat,
            self.lon,
            state,
            config,
            virtual_world,
            simulation_settings,
            deployment_days
        )

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
                    # Only record and fix leaks on the last day of work if there is rollover
                    self.visit_site(site_plan['site'])
                    # Update the cost per site once the site is done surveying
                    self.daily_cost += self.config['cost']['per_site']
                self.worked_today = True
                # NOTE Mobile LDAR_mins also includes travel to site time
                self.state['t'].current_date += timedelta(
                    minutes=int(site_plan['LDAR_mins']))
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
        elif self.config['is_follow_up']:
            site.update({'currently_flagged': False})
            if site_detect_results['found_leak'] and \
                    (self.config['measurement_scale'].lower() == 'site' or
                     self.config['measurement_scale'].lower() == "equipment"):
                self.timeseries['{}_sites_vis_w_leaks'.format(m_name)][cur_ts] += 1
                self.candidate_flags.append(site_detect_results)
        elif site_detect_results['found_leak']:
            # all other sites flag
            self.timeseries['{}_sites_vis_w_leaks'.format(m_name)][cur_ts] += 1
            self.candidate_flags.append(site_detect_results)

        # Record results of site visit
        if self.simulation_settings[OUTPUTS][SITE_VISITS]:
            site_vis_rec = self.gen_site_vis_rec(site_detect_results, site)
            self.state['site_visits'][self.config['label']].append(site_vis_rec)

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
        covered_site_rate: float = 0
        site_rate: float = 0
        covered_equipment_rates = [0] * int(site['equipment_groups'])
        equipment_rates = [0] * int(site['equipment_groups'])
        for leak in site['active_leaks']:
            leak: FugitiveEmission
            leak_rate: float = leak.get_rate()
            # Check to see if leak is spatially covered
            if leak.check_spatial_cov(m_name, self.config['coverage']['spatial']):
                # Check to see if leak is temporally covered
                if np.random.binomial(1, self.config['coverage']['temporal']):
                    covered_leaks.append(leak)
                    covered_site_rate += leak_rate
                    covered_equipment_rates[leak.get_equip_grp() - 1] += leak_rate
            site_rate += leak_rate
            equipment_rates[leak.get_equip_grp() - 1] += leak_rate
            # Get the type of sensor, and call the detect emissions function for sensor
            # Aggregate true emissions to equipment and site level; get list of leaks present

        # Add vented emissions
        venting = 0
        if self.consider_venting:
            if 'empirical_vent_rates' in site:
                venting = random.choice(site['empirical_vent_rates'])
            else:
                venting = site['static_venting_rate']
            covered_site_rate += venting
            site_rate += venting
            for rate in range(len(covered_equipment_rates)):
                covered_equipment_rates[rate] += venting / int(site['equipment_groups'])
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

    def gen_site_vis_rec(self, site_detect_results, site) -> Dict[str, Any]:
        """Returns a dictionary tracking key results from a crews visit to a site.

        Results tracked in the dictionary consist of the date of the site visit,
        the ID of the site visited, the site subtype code, the site true emissions rate,
        the site measured emissions rate, the site vent rate, whether a leak was found,
        the ID of the crew that visited the site and;  the leak ID, rate spatial coverage,
        temporal coverage, the date tagged and tag status of every leak at the site.

        Args:
            site_detect_results (dict): Dictionary with the emissions detection results at the site
            site (dict): The site that was visited

        Returns:
            dict[str, Any]: A dictionary of key results from the site visit
        """
        m_name = self.config['label']
        site_vis_rec = {
            'site_vis_date': self.state['t'].current_date.strftime('%Y-%m-%d'),
            'site_visited': site['facility_ID'],
            'site_subtype_code': site['subtype_code'],
            'leaks_at_site': [{k: v for k, v in leak.items() if k in
                               ['leak_ID', 'rate', f'{m_name}_sp_covered', 'tagged', 'date_tagged']}
                              for leak in site['active_leaks']],
            'site_true_rate': site_detect_results['site_true_rate'],
            'site_measured_rate': site_detect_results['site_measured_rate'],
            'site_vent_rate': site_detect_results['vent_rate'],
            'found_leak': site_detect_results['found_leak'],
            'crew_ID': self.id,
        }
        for leak in site_vis_rec['leaks_at_site']:
            if any(dictionary.get('leak_ID') == leak['leak_ID']
                    for dictionary in site_detect_results['leaks_present']):
                leak[f'{m_name}_survey_tp_covered'] = 1
            else:
                if leak[f'{m_name}_sp_covered'] == 1:
                    leak[f'{m_name}_survey_tp_covered'] = 0
                else:
                    leak[f'{m_name}_survey_tp_covered'] = 'N/A'

        return site_vis_rec
