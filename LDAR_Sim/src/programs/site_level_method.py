from initialization.sites import Site
from scheduling.schedules import GenericSchedule


class SiteLevelMethod:
    def __init__(self, name, properties):
        super().__init__(name, properties)

    def survey_site(self, site: Site):
        # TODO complete this method
        # if detection and will_followup:
        #     self.flag_site(site)
        return

    def flag_site(self, site: Site, follow_up_schedule: GenericSchedule):
        # TODO complete this method
        return
