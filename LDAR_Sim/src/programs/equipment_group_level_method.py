from virtual_world.sites import Site
from scheduling.generic_schedule import GenericSchedule


class EquipmentGroupLevelMethod:
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
