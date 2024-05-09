from typing import Any


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
        if hasattr(self, f"_{key}"):
            setattr(self, f"_{key}", value)
        else:
            raise AttributeError(f"Attribute {key} not found")

    def alter_parameters(self, parameters: dict[str, Any]):
        for key, value in parameters.items():
            self.alter_parameter(key, value)

    def get_parameter_value(self, key: str) -> Any:
        if hasattr(self, f"_{key}"):
            return getattr(self, f"_{key}")
        else:
            raise AttributeError(f"Attribute {key} not found")

    def override_parameters(self, parameters: dict[str, Any]):
        for key, value in parameters.items():
            self.override_parameter(key, value)

    def override_parameter(self, key: str, value: Any):
        if hasattr(self, f"_{key}"):
            if isinstance(getattr(self, f"_{key}"), type(value)):
                setattr(self, f"_{key}", value)
            else:
                raise TypeError(f"Type mismatch for attribute {key}")
        else:
            raise AttributeError(f"Attribute {key} not found")

    def delete_parameter(self, key: str):
        if hasattr(self, f"_{key}"):
            delattr(self, f"_{key}")
        else:
            raise AttributeError(f"Attribute {key} not found")

    def add_parameter(self, key: str, value: Any):
        setattr(self, f"_{key}", value)

    def get_parameter(self, key: str) -> Any:
        if hasattr(self, f"_{key}"):
            return getattr(self, f"_{key}")
        else:
            raise AttributeError(f"Attribute {key} not found")
