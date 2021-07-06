# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        fixed_crew
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

import numpy as np

from methods.base_crew import BaseCrew


class StationaryCrew(BaseCrew):
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

    def __init__(self, state, parameters, config, timeseries, site, deployment_days, id):
        super(StationaryCrew, self).__init__(
            state, parameters, config, timeseries, deployment_days, id)
        # --- Travel specific Initalization ---
        self.site = site
        self.days_skipped = 0
        return

    # Overwrite Work A day function
    def work_a_day(self, candidate_flags):
        """
        Go to work and find the leaks for a given day
        """
        self.candidate_flags = candidate_flags
        m_name = self.config['label']
        # Sum all the emissions at the site
        leaks_present = []
        site_cum_rate = 0

        for leak in self.state['leaks']:
            if leak['facility_ID'] == self.site['facility_ID']:
                if leak['status'] == 'active':
                    if leak['days_active'] >= \
                            (self.config['time_to_detection'] + self.days_skipped):
                        leaks_present.append(leak)
                        site_cum_rate += leak['rate']

        # Add vented emissions
        venting = 0
        if self.parameters['consider_venting']:
            venting = self.state['empirical_vents'][
                np.random.randint(0, len(self.state['empirical_vents']))]
            site_cum_rate += venting

        # Simple detection module based on strict minimum detection limit
        detect = False
        if site_cum_rate > (self.config['MDL']):
            detect = True

        if detect:
            # If source is above follow-up threshold, calculate measured rate using
            # quantification error
            quant_error = np.random.normal(0, self.config['QE'])
            measured_rate = None
            if quant_error >= 0:
                measured_rate = site_cum_rate + site_cum_rate*quant_error
            if quant_error < 0:
                denom = abs(quant_error - 1)
                measured_rate = site_cum_rate/denom

            # If source is above follow-up threshold
            if measured_rate > self.config['follow_up_thresh']:
                # Put all necessary information in a dictionary to be assessed at end of day
                site_dict = {
                    'site': self.site,
                    'leaks_present': leaks_present,
                    'site_true_rate': site_cum_rate,
                    'site_measured_rate': measured_rate,
                    'venting': venting
                }

                self.candidate_flags.append(site_dict)

        self.timeseries['{}_cost'.format(m_name)][self.state['t'].current_timestep] += \
            self.config['cost_per_day']

        self.timeseries['total_daily_cost'][self.state['t'].current_timestep] += \
            self.config['cost_per_day']

        return
