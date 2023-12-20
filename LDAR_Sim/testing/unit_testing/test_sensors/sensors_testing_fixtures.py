import pytest

from sensors.default_site_level_sensor import DefaultSiteLevelSensor


@pytest.fixture(name="sensor_info_for_default_site_level_sensor_construction_testing")
def sensor_info_for_default_site_level_sensor_construction_testing_fix() -> dict[str, int]:
    return {"mdl": 1}


@pytest.fixture(name="sensor_for_default_site_level_sensor_testing")
def sensor_for_default_site_level_sensor_testing_fix() -> DefaultSiteLevelSensor:
    mdl: float = 1.0
    return DefaultSiteLevelSensor(mdl=mdl)
