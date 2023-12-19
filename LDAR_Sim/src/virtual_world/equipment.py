import copy
import datetime
import re

from virtual_world.emissions import Emission
from virtual_world.infrastructure_const import Infrastructure_Constants

from virtual_world.sources import Source

SOURCE_CREATION_ERROR_MESSAGE = (
    "Invalid LDAR-Sim infrastructure inputs: Failure to read in sources infrastructure input"
)


class Equipment:
    def __init__(self, equip_type, equip_id, infrastructure_inputs, prop_params) -> None:
        STR_FILTER = r"_equipment"
        pattern: re.Pattern[str] = re.compile(re.escape(STR_FILTER), re.IGNORECASE)
        self._equip_type: str = re.sub(pattern, "", equip_type)
        self._equipment_ID: str = self._equip_type + "_" + str(equip_id)
        self.create_sources(infrastructure_inputs=infrastructure_inputs, prop_params=prop_params)

    def create_sources(self, infrastructure_inputs, prop_params) -> None:
        self._sources: list[Source] = []
        if self._equip_type != "Placeholder" and "sources" in infrastructure_inputs:
            sources_info = infrastructure_inputs["sources"]
            sources = sources_info.loc[
                sources_info[Infrastructure_Constants.Sources_File_Constants.EQUIPMENT]
                == self._equip_type
            ]
            for source in sources:
                src_prop_params = copy.deepcopy(prop_params)
                src_id = source[Infrastructure_Constants.Sources_File_Constants.SOURCE]
                self._sources.append(Source(src_id, source, src_prop_params))
        elif self._equip_type == "Placeholder":
            src_id = "Placeholder_Non_Rep"
            placeholder_source_info = {
                Infrastructure_Constants.Sources_File_Constants.REPAIRABLE: True,
                Infrastructure_Constants.Sources_File_Constants.PERSISTENT: True,
                Infrastructure_Constants.Sources_File_Constants.ACTIVE_DUR: 1,
                Infrastructure_Constants.Sources_File_Constants.INACTIVE_DUR: 0,
            }
            self._sources.append(Source(src_id, placeholder_source_info, prop_params))
        else:
            print(SOURCE_CREATION_ERROR_MESSAGE)

    def generate_emissions(self, sim_start_date, sim_end_date, sim_number) -> dict:
        equip_emissions = {}
        for src in self._sources:
            equip_emissions.update(src.generate_emissions(sim_start_date, sim_end_date, sim_number))

        return {self._equipment_ID: equip_emissions}

    def activate_emissions(self, date: datetime, sim_number: int) -> None:
        """Activate any emissions that are due to begin on the current date for the given simulation
        and add them to the active emissions list for the equipment at which they occur.

        Args:
            date (datetime): The current date in simulation.
            sim_number (int): The simulation number.
            Used to interact with the correct set of emissions.
        """
        self._active_emissions: list[Emission] = []
        for source in self._sources:
            new_emissions: list[Emission] = source.activate_emissions(date, sim_number)
            self._active_emissions.extend(new_emissions)

    def get_detectable_emissions(self, method_name: str) -> Emission:
        detectable_emissions: list[Emission] = []
        for emis in self._active_emissions:
            if emis.check_spatial_cov(method_name):
                detectable_emissions.append(emis)

        return detectable_emissions

    def set_pregen_emissions(self, equipment_emissions, sim_number) -> None:
        for src in self._sources:
            src.set_pregen_emissions(equipment_emissions[src.get_id()], sim_number)

    def get_id(self) -> str:
        return self._equipment_ID
