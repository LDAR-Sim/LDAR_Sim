from datetime import datetime
from virtual_world.emissions import Emission
from virtual_world.infrastructure_const import Infrastructure_Constants
from virtual_world.equipment import Equipment


class Equipment_Group:
    def __init__(self, id, infrastructure_inputs, prop_params, info) -> None:
        self._id: str = id
        self.update_prop_params(info, prop_params)
        self.set_method_specific_params(prop_params)
        self.create_equipment(
            infrastructure_inputs=infrastructure_inputs, prop_params=prop_params, info=info
        )

    def update_prop_params(self, info, prop_params) -> None:
        meth_specific_params = prop_params.pop("Method_Specific_Params")

        for param in meth_specific_params.keys():
            for method in meth_specific_params[param].keys():
                eqg_val = info.get(method + param, None)
                if eqg_val is not None:
                    meth_specific_params[param][method] = eqg_val

        for param in prop_params.keys():
            eqg_val = info.get(param, None)
            if eqg_val is not None:
                prop_params[param] = eqg_val

        prop_params["Method_Specific_Params"] = meth_specific_params

    def create_equipment(self, infrastructure_inputs, prop_params, info) -> None:
        self._equipment: list[Equipment] = []
        for col, val in info.items():
            if "equipment" in col.lower():
                for count in range(0, val):
                    self._equipment.append(
                        Equipment(col, count, infrastructure_inputs, prop_params)
                    )

    def set_method_specific_params(self, prop_params):
        self._meth_survey_times = prop_params["Method_Specific_Params"].pop(
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_TIME_PLACEHOLDER
        )
        self._meth_survey_costs = prop_params["Method_Specific_Params"].pop(
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_COST_PLACEHOLDER
        )

    def generate_emissions(self, sim_start_date, sim_end_date, sim_number) -> dict:
        eqg_emissions = {}
        for eqmt in self._equipment:
            eqg_emissions.update(eqmt.generate_emissions(sim_start_date, sim_end_date, sim_number))

        return {self._id: eqg_emissions}

    def activate_emissions(self, date: datetime, sim_number: int) -> None:
        """Activate any emissions that are due to begin on the current date for the given simulation
        and add them to the active emissions list for the equipment at which they occur.

        Args:
            date (datetime): The current date in simulation.
            sim_number (int): The simulation number.
            Used to interact with the correct set of emissions.
        """
        for equipment in self._equipment:
            equipment.activate_emissions(date, sim_number)

    def get_detectable_emissions(self, method_name: str) -> dict[str, list[Emission]]:
        detectable_emissions: dict[str, Emission] = {}
        for equip in self._equipment:
            detectable_emissions[equip.get_id()] = equip.get_detectable_emissions(method_name)

        return detectable_emissions

    def set_pregen_emissions(self, eqg_emissions, sim_number) -> None:
        for equipment in self._equipment:
            equipment.set_pregen_emissions(eqg_emissions[equipment.get_id()], sim_number)

    def get_survey_time(self, method_name) -> float:
        survey_time: float = self._meth_survey_times[method_name]
        return survey_time

    def report_func(self):
        # some reporting agregate function?
        return

    def get_id(self) -> str:
        return self._id
