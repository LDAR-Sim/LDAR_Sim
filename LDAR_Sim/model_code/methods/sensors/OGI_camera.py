import numpy as np
import math


def detect_emissions(self, site, leaks_present, equipment_rates, site_true_rate, venting):
    for leak in leaks_present:
        k = np.random.normal(4.9, 0.3)
        x0 = np.random.normal(self.config['MDL'][0], self.config['MDL'][1])
        x0 = math.log10(x0 * 3600)  # Convert from g/s to g/h and take log

        if leak['rate'] == 0:
            prob_detect = 0
        else:
            x = math.log10(leak['rate'] * 3600)  # Convert from g/s to g/h
            prob_detect = 1 / (1 + math.exp(-k * (x - x0)))
        detect = np.random.binomial(1, prob_detect)

        if detect:
            if leak['tagged']:
                self.timeseries[self.config['label'] +
                                '_redund_tags'][self.state['t'].current_timestep] += 1

            # Add these leaks to the 'tag pool'
            elif not leak['tagged']:
                leak['tagged'] = True
                leak['date_tagged'] = self.state['t'].current_date
                leak['tagged_by_company'] = self.config['label']
                leak['tagged_by_crew'] = self.id
                self.state['tags'].append(leak)

        elif not detect:
            site[self.config['label'] + '_missed_leaks'] += 1

    return
