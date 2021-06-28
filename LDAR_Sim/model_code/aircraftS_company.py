
# from generic_functions import get_prop_rate
from methods.base_company import company
from methods.base_crew import crew


class aircraftS_company(company):
    def __init__(self, state, parameters, config, timeseries):
        # Run The base class Init
        super(aircraftS_company, self).__init__(state, parameters, config, timeseries)
        # ---------company-level scheduling------

        # Initiate Crews
        for i in range(config['n_crews']):
            self.crews.append(crew(state, parameters, config,
                                   timeseries, self.deployment_days, id=i + 1))
