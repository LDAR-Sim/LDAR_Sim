

from methods.company import BaseCompany
from methods.crew import BaseCrew


class dev_OGI_company(BaseCompany):
    """ Test Company module. Company managing fixed agents.
        Inherits base method base class company
    """

    def __init__(self, state, parameters, config, timeseries):
        super(dev_OGI_company, self).__init__(state, parameters, config, timeseries)
        # --- Custom Init ---
        # -------------------

    # --- Custom Methods ---
    # ----------------------


class Crew(BaseCrew):
    """ Test Company module. Initialize each crew for company.
        Inherits base method base class company

    OGI has a unique method of detection, so default visit_site routine
    is overwritten.
    """

    def __init__(self, state, parameters, config, timeseries, deployment_days, id):
        super(Crew, self).__init__(state, parameters, config, timeseries, deployment_days, id)
        # --- Custom Init ---
        # -------------------
