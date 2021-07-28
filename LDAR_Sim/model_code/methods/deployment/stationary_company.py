import math
from methods.deployment._base import SchedCompany as BaseSchedCompany
from methods.crew import BaseCrew


def make_crews(crews, config, state, parameters, timeseries, deployment_days):
    m_name = config['label']
    for site in state['sites']:
        if config['measurement_scale'] == "equipment":  # This may change in the future
            n_fixed = int(site['fixed_sensors'])
        else:
            n_fixed = int(site['fixed_sensors'])
        for i in range(n_fixed):
            crew_ID = site['facility_ID'] + '-' + str(i + 1)
            # Will only accept the first crew assigned to site
            if not site['crew_ID']:
                site.update({'crew_ID': crew_ID})
            crews.append(
                BaseCrew(
                    state,
                    parameters,
                    config,
                    timeseries,
                    deployment_days,
                    id=crew_ID,
                    site))
            timeseries['{}_cost'.format(m_name)][state['t'].current_timestep] += \
                config['up_front_cost']


class Schedule(BaseSchedCompany):
    def __init__(self, config, parameters, state):
        self.parameters = parameters
        self.config = config
        self.state = state

    # --- inherited ---
    # base.company ->  get_deployment_dates()
    # base.company ->  can_deploy_today()

    def assign_agents(self):
        pass

    def get_due_sites(self, site_pool):
        """[summary]

        Args:
            site_pool ([type]): [description]

        Returns:
            [type]: [description]
        """
        # site = [site for site in site_pool if site['facility_ID'] == self.site['facility_ID']]
        return site_pool

    def get_working_crews(self, site_pool,  self.crews):
        # Passes sites with assigned crews (crew ID)
        site_pool = [site for site in site_pool if site['crew_ID']]
        n_working_crews = len(site_pool)
        return n_working_crews, site_pool

    def get_crew_site_list(self, site_pool, crew_idx, n_crews):
        """[summary]

        Args:
            site_pool ([type]): [description]
            crew_ID ([type]): [description]
            n_crews ([type]): [description]

        Returns:
            [type]: [description]
        """
        return site_pool[crew_idx]
