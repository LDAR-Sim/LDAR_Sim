from sensors.default_sensor import DefaultSensor


class DefaultSiteLevelSensor(DefaultSensor):
    def __init__(self, mdl: float) -> None:
        super().__init__(mdl)
