import numpy as np


def detect_emissions(self, site, leaks_present, equipment_rates, site_true_rate, venting):
    for leak in leaks_present:
        if leak['rate'] > self.config['MDL'] \
                and (np.random.random() > (1 - self.config['percent_detectable'])):
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

        else:
            site[self.config['label'] + '_missed_leaks'] += 1
    return None
