class Schedule:
    def __init__(self, meta):
        self.meta = meta

    def get_deployment_dates(self, state_t):
        # if user does not specify deployment interval, set to all months/years
        if len(self.meta['deployment_years']) > 0:
            self.deployment_years = self.meta['deployment_years']
        else:
            self.deployment_years = list(
                range(state_t.start_date.year, state_t.end_date.year+1))

        if len(self.meta['deployment_months']) > 0:
            self.deployment_months = self.meta['deployment_months']
        else:
            self.deployment_months = list(range(1, 13))
