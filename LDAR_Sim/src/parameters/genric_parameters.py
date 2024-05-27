# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        generic_parameters.py
# Purpose:     A generic class to hold parameter values
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
from typing import Any
from constants import sensitivity_analysis_constants as sens_const


class GenericParameters:
    def __init__(self, parameters: dict[str, Any]) -> None:
        for key, setting in parameters.items():
            setattr(self, f"_{key}", setting)

    def to_dict(self):
        return {
            attr_name[1:]: value
            for attr_name, value in self.__dict__.items()
            if attr_name.startswith("_")
        }

    def alter_parameter(self, key: str, value: Any):
        attribute_name: str = f"_{key}"
        if hasattr(self, attribute_name):
            setattr(self, attribute_name, value)
        else:
            raise AttributeError(sens_const.ParameterParsingConstants.KEY_NOT_FOUND.format(key=key))

    def alter_parameters(self, parameters: dict[str, Any]):
        for key, value in parameters.items():
            self.alter_parameter(key, value)

    def get_parameter(self, key: str) -> Any:
        attribute_name: str = f"_{key}"
        if hasattr(self, attribute_name):
            return getattr(self, attribute_name)
        else:
            raise AttributeError(sens_const.ParameterParsingConstants.KEY_NOT_FOUND.format(key=key))

    def get_parameter_value(self, key: str):
        return self.get_parameter(key)

    def override_parameters(self, parameters: dict[str, Any]):
        for key, value in parameters.items():
            self.override_parameter(key, value)

    def override_parameter(self, key: str, value: Any):
        attribute_name: str = f"_{key}"
        if hasattr(self, attribute_name):
            if isinstance(getattr(self, attribute_name), type(value)):
                setattr(self, attribute_name, value)
            else:
                raise TypeError(sens_const.ParameterParsingConstants.TYPE_MISMATCH.format(key=key))
        else:
            raise AttributeError(sens_const.ParameterParsingConstants.KEY_NOT_FOUND.format(key=key))

    def delete_parameter(self, key: str):
        attribute_name: str = f"_{key}"
        if hasattr(self, attribute_name):
            delattr(self, attribute_name)
        else:
            raise AttributeError(sens_const.ParameterParsingConstants.KEY_NOT_FOUND.format(key=key))

    def add_parameter(self, key: str, value: Any):
        setattr(self, f"_{key}", value)
