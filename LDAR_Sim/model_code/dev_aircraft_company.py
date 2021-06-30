from methods.travel_company import travel_company
from methods.travel_crew import travel_crew


class dev_aircraft_company(travel_company):
    """ Test aircraft company module. Company managing fixed agents.
        Inherits base method base class company
    """

    def __init__(self, state, parameters, config, timeseries):
        super(dev_aircraft_company, self).__init__(state, parameters, config, timeseries)
        # --- Custom Init ---
        # -------------------
        # Initiate Crews - This is done outside of base class
        for i in range(config['n_crews']):
            self.crews.append(crew(state, parameters, config,
                                   timeseries, self.deployment_days, id=i + 1))

    # --- Custom Methods ---
    # ----------------------


class crew(travel_crew):
    """ Test Company module. Initialize each crew for company.
        Inherits base method base class company
    """

    def __init__(self, state, parameters, config, timeseries, deployment_days, id):
        super(crew, self).__init__(state, parameters, config, timeseries, deployment_days, id)
        # --- Custom Init ---
        # -------------------

    # --- Custom Methods ---
    # ----------------------
