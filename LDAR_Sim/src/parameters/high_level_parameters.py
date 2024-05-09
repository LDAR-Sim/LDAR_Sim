from typing import Any, override

from parameters.genric_parameters import GenericParameters


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
            else:
                setattr(self, f"_{key}", value)
        else:
            raise AttributeError(f"Attribute {key} not found")

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
            raise AttributeError(f"Attribute {key} not found")
