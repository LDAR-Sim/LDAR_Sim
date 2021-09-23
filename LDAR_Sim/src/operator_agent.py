# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Operator
# Purpose:     Initialize and manage operator detection module
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

import numpy as np


class OperatorAgent:
    def __init__(self, timeseries, parameters, state):
        """
        Constructs an operator who visits all sites and occasionally finds
        a leak.
        """
        self.parameters = parameters
        self.state = state
        self.timeseries = timeseries
        self.init_mean_leaks = np.mean(self.state['init_leaks'])
        self.init_sum_leaks = np.sum(self.state['init_leaks'])
        self.n_sites = len(self.state['sites'])

        return

    def work_a_day(self):
        """
        Detect leaks during operator visits.
        Detection can be a function of leak-size.
        """

        active_leaks = self.timeseries['active_leaks'][self.state['t'].current_timestep]
        if active_leaks > 0:
            leak_term = (self.init_sum_leaks / (active_leaks)) * self.init_mean_leaks

            for leak in self.state['leaks']:
                if leak['status'] == 'active':
                    prob_detect = self.parameters['LPR'] * 7 / leak_term
                    prob_detect  \
                        += self.parameters['max_det_op'] \
                        * (leak['rate'] / (self.state['max_leak_rate']))
                    if prob_detect > 1:
                        prob_detect = 1
                    if prob_detect < 0:
                        prob_detect = 0
                    try:
                        prob_detect = prob_detect * self.parameters['operator_strength']
                    except KeyError:
                        prob_detect = 0
                    detect = np.random.binomial(1, prob_detect)

                    if detect:
                        if leak['tagged']:
                            self.timeseries['operator_redund_tags'][
                                self.state['t'].current_timestep] += 1

                        elif not leak['tagged']:
                            # Add these leaks to the 'tag pool'
                            leak['tagged'] = True
                            leak['date_tagged'] = self.state['t'].current_date
                            leak['tagged_by_company'] = 'operator'
                            leak['tagged_by_crew'] = 1
                            self.state['tags'].append(leak)
                            self.timeseries['operator_tags'][self.state['t'].current_timestep] += 1

        return
