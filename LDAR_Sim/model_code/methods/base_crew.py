# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        crew
# Purpose:     Initialize each crew under company
#
# Copyright (C) 2018-2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
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
import numpy as np
from importlib import import_module
from aggregator import aggregate
from geography.distance import get_distance


class BaseCrew:
    """
    Base class crew function. Changes made here will affect any inheriting
    classes. To use base class, import and use as argument arguement. ie.

    from methods.base_crew import base_crew
    class crew (base_crew):
        def __init__(self, **kwargs):
            super(crew, self).__init__(**kwargs)
        ...s

    overwrite methods by creating methods in the inheriting class
    after the __init__ function.
    """

    def __init__(self, state, parameters, config, timeseries, deployment_days, id):
        """
        Constructs an individual crew based on defined configuration.
        """
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.deployment_days = deployment_days
        self.crewstate = {'id': id}
        self.crewstate['lat'] = 0.0
        self.crewstate['lon'] = 0.0
        return

    def choose_site(self, crew_x, crew_y):
        """
        Choose a site to survey.

        """
        m_name = self.config['label']
        if self.config['is_follow_up']:
            site_pool = self.state['flags']
        else:
            site_pool = self.state['sites']
        # Sort all sites based on a neglect ranking
        site_pool = sorted(
            site_pool,
            key=lambda k: k['{}_t_since_last_LDAR'.format(m_name)],
            reverse=True)
        site = None
        facility_ID = None  # The facility ID gets assigned if a site is found
        found_site = False  # The found site flag is updated if a site is found
        travel_time = None
        Site_T = []
        s_list = []

        # Then, starting with the most neglected site, check if conditions are suitable for LDAR
        for site in site_pool:
            s_list.append(site)
            site_x = np.float(site['lon'])
            site_y = np.float(site['lat'])

            # Check to see if the site can be surveyed.
            # If route planning is used the site needs to be assigned to the crew
            if (self.config['scheduling']['route_planning']
                    and site['label'] + 1 == self.crewstate['id']
                    or not self.config['scheduling']['route_planning']):
                if not site['{}_attempted_today?'.format(m_name)]:
                    if self.config['is_follow_up']:
                        is_ready = (self.state['t'].current_date - site['date_flagged']).days \
                            >= self.parameters['methods'][site['flagged_by']]['reporting_delay']
                    else:
                        # If the site is 'unripened' (i.e. hasn't met the minimum interval set
                        # out in the LDAR regulations/policy), break out - no LDAR today
                        if site['{}_t_since_last_LDAR'.format(m_name)]  \
                                < int(site['{}_min_int'.format(m_name)]):
                            self.state['t'].current_date = self.state['t'].current_date.replace(
                                hour=23)
                            break
                        elif site['{}_surveys_done_this_year'.format(m_name)] \
                                < int(site['{}_RS'.format(m_name)]):
                            is_ready = True
                        else:
                            is_ready = False

                    # if the site is ready for survey (schedule, or picked through route planning)
                    if is_ready:
                        # If weather is suitable for crew to survey
                        if self.deployment_days[site['lon_index'],
                                                site['lat_index'],
                                                self.state['t'].current_timestep]:

                            if self.scheduling['geography']:
                                d = get_distance(crew_x, crew_y, site_x, site_y, "Haversine")
                                speed = np.random.choice(self.config['scheduling']['speed_list'])
                                wt = d/speed * 60
                                Site_T.append(wt)
                                # HBD - What happens if there is route planning and geography?
                                if not self.scheduling['route_planning']:
                                    # The site passes all the tests! Choose it!
                                    travel_time = wt
                                    facility_ID = site['facility_ID']
                                    found_site = True
                                    # Update site
                                    site['{}_surveys_conducted'.format(m_name)] += 1
                                    site['{}_surveys_done_this_year'.format(m_name)] += 1
                                    site['{}_t_since_last_LDAR'.format(m_name)] = 0
                                    break
                            else:
                                # The site passes all the tests! Choose it!
                                facility_ID = site['facility_ID']
                                found_site = True
                                travel_time = int(np.random.choice(self.config['t_bw_sites']))
                                # Update site
                                site['{}_surveys_conducted'.format(m_name)] += 1
                                site['{}_surveys_done_this_year'.format(m_name)] += 1
                                site['{}_t_since_last_LDAR'.format(m_name)] = 0
                                break

                        else:
                            site['{}_attempted_today?'.format(m_name)] = True

        if self.scheduling['route_planning']:
            if len(Site_T) > 0:
                j = Site_T.index(min(Site_T))
                site = s_list[j]
                facility_ID = site['facility_ID']
                travel_time = min(Site_T)*60
                found_site = True

                # Update site
                site['{}_surveys_conducted'.format(m_name)] += 1
                site['{}_surveys_done_this_year'.format(m_name)] += 1
                site['{}_t_since_last_LDAR'.format(m_name)] = 0

        return (facility_ID, found_site, site, travel_time)

    def visit_site(self, site, travel_time=None):
        """
        Look for emissions at the chosen site.
        """
        m_name = self.config['label']

        # Aggregate true emissions to equipment and site level; get list of leaks present
        leaks_present, equipment_rates, site_true_rate = aggregate(site, self.state['leaks'])

        # Add vented emissions
        venting = 0
        if self.parameters['consider_venting']:
            venting = self.state['empirical_vents'][
                np.random.randint(0, len(self.state['empirical_vents']))]
        site_true_rate += venting
        for rate in range(len(equipment_rates)):
            equipment_rates[rate] += venting/int(site['equipment_groups'])

        _ = self.detect_emissions(
            site, leaks_present, equipment_rates, site_true_rate, venting)

        # --- Update time ---
        self.state['t'].current_date += timedelta(minutes=int(site['{}_time'.format(m_name)]))
        # if travel time was not generated when choosing site
        if not travel_time:
            travel_time = np.random.choice(self.config['t_bw_sites'])
        self.state['t'].current_date += timedelta(
            minutes=int(travel_time))
        self.timeseries['{}_sites_visited'.format(m_name)][self.state['t'].current_timestep] += 1

        if self.config['is_follow_up']:
            # Remove site from flag pool
            site['currently_flagged'] = False
        return

    def detect_emissions(self, *args):
        # Get the type of sensor, and call the the detect emissions function for sensor
        sensor_mod = import_module('methods.sensors.{}'.format(self.config['sensor']))
        detect_emis_sensor = getattr(sensor_mod, 'detect_emissions')
        is_leak_detected = detect_emis_sensor(self, *args)
        return is_leak_detected
