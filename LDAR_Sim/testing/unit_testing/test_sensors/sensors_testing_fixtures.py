import pytest
from virtual_world.emissions import Emission

from virtual_world.sites import Site


@pytest.fixture(name="sensor_info_for_default_site_level_sensor_construction_testing")
def sensor_info_for_default_site_level_sensor_construction_testing_fix() -> dict[str, int]:
    return {"mdl": 1, "QE": 0.0}


@pytest.fixture(name="mock_site_emis_for_detect_emissions_testing")
def mock_site_emis_for_detect_emissions_testing_fix(mocker):
    ret_vals: list[float] = [1.0, 2.0, 3.0]
    mock_site_emis: dict[str, dict[str, list[Emission]]] = {
        "test_eqg_1": {
            "test_equip_1": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals
            ],
        },
        "test_eqg_2": {
            "test_equip_1": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals
            ],
        },
        "test_eqg_3": {
            "test_equip_1": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals
            ],
        },
    }
    return mock_site_emis


@pytest.fixture(name="mock_site_for_detect_emissions_testing")
def mock_site_for_detect_emissions_testing_fix(mocker, mock_site_emis_for_detect_emissions_testing):
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    mocker.patch.object(
        Site, "get_detectable_emissions", return_value=mock_site_emis_for_detect_emissions_testing
    )
    expected_site_emis = 6 * 9
    return (mocker, expected_site_emis)
