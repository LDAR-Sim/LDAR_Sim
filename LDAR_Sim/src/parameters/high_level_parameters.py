# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        high_level_parameters.py
# Purpose:     A class to hold nested LDAR-Sim parameters
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.


# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------

from typing import Any, override

from parameters.genric_parameters import GenericParameters
from constants import sensitivity_analysis_constants as sens_const


class HighLevelParameters(GenericParameters):
    def __init__(
        self, parameters: dict[str, Any], sub_parameter_mapping: dict[str, None | dict[str, Any]]
    ) -> None:
        params_for_initialization = parameters.copy()
        for key in parameters.keys():
            if key in sub_parameter_mapping.keys():
                values: Any = params_for_initialization.pop(key)
                sub_mapping_vals = sub_parameter_mapping[key]
                if isinstance(sub_mapping_vals, dict):
                    setattr(self, f"_{key}", HighLevelParameters(values, sub_mapping_vals))
                else:
                    setattr(self, f"_{key}", GenericParameters(values))
        super().__init__(params_for_initialization)

    @override
    def to_dict(self):
        return {
            attr_name[1:]: (
                value.to_dict()
                if isinstance(value, (HighLevelParameters, GenericParameters))
                else value
            )
            for attr_name, value in self.__dict__.items()
            if attr_name.startswith("_")
        }

    @override
    def alter_parameter(self, key: str, value: Any):
        if hasattr(self, f"_{key}"):
            attr = getattr(self, f"_{key}")
            if hasattr(attr, "alter_parameters"):
                attr.alter_parameters(value)
            elif isinstance(attr, dict):
                attr.update(value)
            else:
                setattr(self, f"_{key}", value)
        else:
            raise AttributeError(sens_const.ParameterParsingConstants.KEY_NOT_FOUND.format(key=key))

    @override
    def alter_parameters(self, parameters: dict[str, Any]):
        for key, value in parameters.items():
            self.alter_parameter(key, value)

    @override
    def get_parameter_value(self, key: str) -> Any:
        if hasattr(self, f"_{key}"):
            attr = getattr(self, f"_{key}")
            if hasattr(attr, "to_dict"):
                return attr.to_dict()
            else:
                return attr
        else:
            for attr_name, value in self.__dict__.items():
                if attr_name.startswith("_"):
                    if hasattr(value, "get_parameter_value"):
                        try:
                            return value.get_parameter_value(key)
                        except AttributeError:
                            pass
            raise AttributeError(sens_const.ParameterParsingConstants.KEY_NOT_FOUND.format(key=key))
