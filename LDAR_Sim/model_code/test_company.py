
from methods.base_company import company as bcomp
from methods.base_crew import crew as bcrew


class test_company(bcomp):
    """Test Company module. Company managing fixed agents.

    Args:
        bcomp (class): Inherited base company
    """

    def __init__(self, state, parameters, config, timeseries):
        # Run The base class Init
        super(test_company, self).__init__(state, parameters, config, timeseries)
        # --------- Add custom functionality Here! ----------------

        # ---------------------------------------------------------
        # Initiate Crews - This is done outside of base class
        for i in range(config['n_crews']):
            self.crews.append(crew(state, parameters, config,
                                   timeseries, self.deployment_days, id=i + 1))


class crew(bcrew):
    """Test Company module. Initialize each crew for company.

    Args:
        bcrew (class): Inherited base crew
    """

    def __init__(self, state, parameters, config, timeseries, deployment_days, id):
        super(crew, self).__init__(state, parameters, config, timeseries, deployment_days, id)
