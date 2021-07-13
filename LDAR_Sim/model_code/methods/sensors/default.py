
from method_functions import measured_rate


def detect_emissions(self, site, leaks_present, equipment_rates, site_true_rate, venting):
    m_name = self.config['label']
    site_measured_rate = 0

    if self.config["measurement_scale"] == "site":
        if site_true_rate > (self.config['MDL']):
            # If source is above follow-up threshold, calculate measured rate using QE
            site_measured_rate = measured_rate(site_true_rate, self.config['QE'])
    elif self.config["measurement_scale"] == "equipment":
        for rate in equipment_rates:
            if rate > (self.config['MDL']):
                equip_measured_rate = measured_rate(rate, self.config['QE'])
                site_measured_rate += equip_measured_rate
    elif self.config["measurement_scale"] == "leak":
        # If measurement scale is a leak, all leaks will be tagged
        for leak in leaks_present:
            if leak['rate'] > (self.config['MDL']):
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
                    site_measured_rate += measured_rate(leak['rate'], self.config['QE'])
            else:
                site[self.config['label'] + '_missed_leaks'] += 1

    # If source is above follow-up threshold
    if site_measured_rate > self.config['follow_up_thresh']:
        # Put all necessary information in a dictionary to be assessed at end of day
        site_dict = {
            'site': site,
            'leaks_present': leaks_present,
            'site_true_rate': site_true_rate,
            'site_measured_rate': site_measured_rate,
            'venting': venting
        }
        # self.candidate_flags.append(site_dict)

    else:
        site_dict = None
        site['{}_missed_leaks'.format(m_name)] += len(leaks_present)

    return site_dict
