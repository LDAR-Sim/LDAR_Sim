
import math
from numpy.random import normal, binomial

from methods.mobile_company import MobileCompany
from methods.mobile_crew import MobileCrew


class dev_OGI_company(MobileCompany):
    """ Test Company module. Company managing fixed agents.
        Inherits base method base class company
    """

    def __init__(self, state, parameters, config, timeseries):
        super(dev_OGI_company, self).__init__(state, parameters, config, timeseries)
        # --- Custom Init ---
        # -------------------
        # Initiate Crews - This is done outside of base class
        for i in range(config['n_crews']):
            self.crews.append(Crew(state, parameters, config,
                                   timeseries, self.deployment_days, id=i + 1))

    # --- Custom Methods ---
    # ----------------------


class Crew(MobileCrew):
    """ Test Company module. Initialize each crew for company.
        Inherits base method base class company

    OGI has a unique method of detection, so default visit_site routine
    is overwritten.
    """

    def __init__(self, state, parameters, config, timeseries, deployment_days, id):
        super(Crew, self).__init__(state, parameters, config, timeseries, deployment_days, id)
        # --- Custom Init ---
        # -------------------

    # --- Custom Methods ---
    def detect_emissions(self, site, leaks_present, equipment_rates, site_true_rate, venting):
        # OGI camera is different then default simple threshold so overwrite detect_emissions
        is_leak_detected = False
        for leak in leaks_present:
            k = normal(4.9, 0.3)
            x0 = normal(self.config['MDL'][0], self.config['MDL'][1])
            x0 = math.log10(x0 * 3600)  # Convert from g/s to g/h and take log

            if leak['rate'] == 0:
                prob_detect = 0
            else:
                x = math.log10(leak['rate'] * 3600)  # Convert from g/s to g/h
                prob_detect = 1 / (1 + math.exp(-k * (x - x0)))
            detect = binomial(1, prob_detect)

            if detect:
                is_leak_detected = True
                if leak['tagged']:
                    self.timeseries[self.config['label'] +
                                    '_redund_tags'][self.state['t'].current_timestep] += 1

                # Add these leaks to the 'tag pool'
                elif not leak['tagged']:
                    leak['tagged'] = True
                    leak['date_tagged'] = self.state['t'].current_date
                    leak['tagged_by_company'] = self.config['label']
                    leak['tagged_by_crew'] = self.crewstate['id']
                    self.state['tags'].append(leak)
            else:
                site[self.config['label'] + '_missed_leaks'] += 1
        return is_leak_detected
    # ----------------------
