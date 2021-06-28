
import math
from datetime import timedelta
from numpy.random import choice, normal, binomial

from methods.base_company import company as bcomp
from methods.base_crew import crew as bcrew


class test_OGI_company(bcomp):
    """Test Company module. Company managing fixed agents.

    Args:
        bcomp (class): Inherited base company
    """

    def __init__(self, state, parameters, config, timeseries):
        # Run The base class Init
        super(test_OGI_company, self).__init__(state, parameters, config, timeseries)
        # --------- Add custom functionality Here! ----------------

        # ---------------------------------------------------------
        # Initiate Crews - This is done outside of base class
        for i in range(config['n_crews']):
            self.crews.append(crew(state, parameters, config,
                                   timeseries, self.deployment_days, id=i + 1))


class crew(bcrew):
    """Test Company module. Initialize each crew for company.
    OGI has a unique method of detection, so default visit_site routine
    is overwritten.

    Args:
        bcrew (class): Inherited base crew
    """

    def __init__(self, state, parameters, config, timeseries, deployment_days, id):
        super(crew, self).__init__(state, parameters, config, timeseries, deployment_days, id)
        # --------- Add custom functionality Here! ----------------

    def visit_site(self, site, travel_time=None):
        m_name = self.config['name']
        """
        Look for leaks at the chosen site.
        """

        # Identify all the leaks at a site
        leaks_present = []
        for leak in self.state['leaks']:
            if leak['facility_ID'] == site['facility_ID']:
                if leak['status'] == 'active':
                    leaks_present.append(leak)

        # Use an OGI camera to detect leaks
        self.detect_leaks(site, leaks_present)

        self.state['t'].current_date += timedelta(minutes=int(site['{}_time'.format(m_name)]))
        self.state['t'].current_date += timedelta(
            minutes=int(choice(self.config['t_bw_sites'])))
        self.timeseries['{}_sites_visited'.format(m_name)][self.state['t'].current_timestep] += 1

        if self.config['is_follow_up']:
            # Remove site from flag pool
            site['currently_flagged'] = False
        return

    def detect_leaks(self, site, leaks):
        for leak in leaks:
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
                if leak['tagged']:
                    self.timeseries[self.config['name'] +
                                    '_redund_tags'][self.state['t'].current_timestep] += 1

                # Add these leaks to the 'tag pool'
                elif not leak['tagged']:
                    leak['tagged'] = True
                    leak['date_tagged'] = self.state['t'].current_date
                    leak['tagged_by_company'] = self.config['name']
                    leak['tagged_by_crew'] = self.crewstate['id']
                    self.state['tags'].append(leak)

            elif not detect:
                site[self.config['name'] + '_missed_leaks'] += 1
    # ---------------------------------------------------------
