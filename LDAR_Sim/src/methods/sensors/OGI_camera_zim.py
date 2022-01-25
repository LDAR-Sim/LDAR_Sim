# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.deployment.OGI_camera_zim
# Purpose:     OGI company specific deployment classes and methods based on zimmerle (2020)
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
from methods.funcs import measured_rate
from utils.attribution import update_tag


def detect_emissions(self, site, covered_leaks, covered_equipment_rates, covered_site_rate,
                     site_rate, venting, equipment_rates):
    """ OGI camera method based on Zimmerlie 2020 DOI 10.1021/acs.est.0c01285
        uses power function as shown in figure 2 to calculate probability of
        detection using leak size and  two mdl parameters are set based on which
        are based on camera crew experience.

    Args:
        site (site obj): Site in which crew is working at
        covered_leaks (list): list of leak objects that can be detected by the crew
        covered_equipment_rates (list): list of equipment leak rates that can be
                                        detected by the crew
        covered_site_rate (float): total site emissions from leaks that are observable
                                    from a crew
        site_rate (float): total site emissions from leaks all leaks at site
        venting (float): total site emissions from venting
        equipment_rates (list): list of equipment leak rates for each equipment group

    Returns:
        site report (dict):
                site  (site obj): same as input
                leaks_present (list): same as covered leaks input
                site_true_rate (float): same as site_rate
                site_measured_rate (float): total emis from all leaks measured
                equip_measured_rates (list): total of all leaks measured for each equip group
                venting (float): same as input
                found_leak (boolean): Did the crew find at least one leak at the site


    """
    missed_leaks_str = '{}_missed_leaks'.format(self.config['label'])
    equip_measured_rates = []
    site_measured_rate = 0
    found_leak = False
    mdl = self.config['sensor']['MDL']
    for leak in covered_leaks:
        # factor of 187 converts g/s to scf/h
        prob_detect = mdl[0] * (187*leak['rate'])**mdl[1]
        if prob_detect >= 1:
            prob_detect = 1
        if np.random.binomial(1, prob_detect):
            found_leak = True
            is_new_leak = update_tag(leak, site, self.timeseries, self.state['t'],
                                     self.config['label'], self.id)
            if is_new_leak:
                site_measured_rate += measured_rate(leak['rate'], self.config['sensor']['QE'])
        else:
            site[missed_leaks_str] += 1
            self.timeseries[missed_leaks_str][self.state['t'].current_timestep] += 1

    site_dict = {
        'site': site,
        'leaks_present': covered_leaks,
        'site_true_rate': site_rate,
        'site_measured_rate': site_measured_rate,
        'equip_measured_rates': equip_measured_rates,
        'vent_rate': venting,
        'found_leak': found_leak,
    }
    return site_dict
