

from methods.base_company import BaseCompany
from methods.mobile_crew import MobileCrew


class dev_OGI_company(BaseCompany):
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
