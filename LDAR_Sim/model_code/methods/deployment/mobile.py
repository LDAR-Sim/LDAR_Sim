from datetime import timedelta
import numpy as np


def check_rollover(self, travel_home_time=None):
    # Check if there is a partially finished site from yesterday
    if len(self.rollover) > 0:
        # Check to see if the remainder of this site can be finished today
        # (if not, this one is huge!) projection includes the time it would
        #  time to drive back to the home base
        if not travel_home_time:
            travel_home_time = timedelta(minutes=int(np.random.choice(self.config['t_bw_sites'])))
        projected_end_time = self.state['t'].current_date + \
            timedelta(minutes=int(self.rollover[1]))

        if (projected_end_time + travel_home_time) > self.allowed_end_time:
            # There's not enough time left for that site today -
            #  get started and figure out how much time remains
            minutes_remaining = (projected_end_time - self.allowed_end_time).total_seconds()/60
            self.rollover = []
            self.rollover.append(self.rollover[0])
            self.rollover.append(minutes_remaining)
            self.state['t'].current_date = self.allowed_end_time
            self.worked_today = True
        elif (projected_end_time + travel_home_time) <= self.allowed_end_time:
            # Looks like we can finish off that site today
            self.visit_site(self.rollover[0])
            self.rollover = []
            self.worked_today = True
    return self.worked_today


def choose_site(self):
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

    # Then, starting with the most neglected site, check if conditions are suitable for LDAR
    for site in site_pool:
        if not site['{}_attempted_today?'.format(m_name)]:
            # hasn't met the minimum interval set  out in the LDAR regulations/policy),
            # break out - no LDAR today . Sites are sorted,sub sebsequent will not meet
            # Criteria either.
            if self.config['is_follow_up']:
                is_ready = (self.state['t'].current_date - site['date_flagged']).days >= \
                    self.parameters['methods'][site['flagged_by']]['reporting_delay']

            else:
                if site['{}_t_since_last_LDAR'.format(m_name)] \
                        < int(site['{}_min_int'.format(m_name)]):
                    self.state['t'].current_date = self.state['t'].current_date.replace(hour=23)
                    break
                # Else if site-specific required visits have not been met for the year
                elif site['{}_surveys_done_this_year'.format(m_name)] \
                        < int(site['{}_RS'.format(m_name)]):
                    is_ready = True
                else:
                    is_ready = False
                    # Check the weather for that site

            if is_ready:
                site['{}_attempted_today?'.format(m_name)] = True
                if self.deployment_days[site['lon_index'],
                                        site['lat_index'],
                                        self.state['t'].current_timestep]:

                    # The site passes all the tests! Choose it!
                    facility_ID = site['facility_ID']
                    found_site = True

                    # Update site
                    site['{}_surveys_conducted'.format(m_name)] += 1
                    site['{}_surveys_done_this_year'.format(m_name)] += 1
                    site['{}_t_since_last_LDAR'.format(m_name)] = 0
                    break
    return (facility_ID, found_site, site)
