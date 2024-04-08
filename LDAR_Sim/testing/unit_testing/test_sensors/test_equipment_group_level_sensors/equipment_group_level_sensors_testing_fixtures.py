from typing import Any, Tuple
import pytest
from src.scheduling.schedule_dataclasses import EquipmentGroupSurveyReport
from src.virtual_world.emissions import Emission

from src.virtual_world.sites import Site


@pytest.fixture(name="sensor_info_for_default_eqg_level_sensor_construction_testing")
def sensor_info_for_default_eqg_level_sensor_construction_testing_fix() -> dict[str, int]:
    return {"mdl": [1], "QE": 0.0}


@pytest.fixture(name="sensor_info_high_mdl_for_default_eqg_level_sensor_testing")
def sensor_info_high_mdl_for_default_eqg_level_sensor_testing_fix() -> dict[str, int]:
    return {"mdl": [2.0], "QE": 0.0}


@pytest.fixture(name="mock_site_emis_for_eqg_level_detect_emissions_testing")
def mock_site_emis_for_eqg_level_detect_emissions_testing_fix(mocker):
    ret_vals: list[float] = [1.0, 2.0, 3.0]
    ret_vals2: list[float] = [4.0, 5.0, 6.0]
    ret_vals3: list[float] = [0.5, 0.5, 0.5]
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
                for retval in ret_vals2
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals2
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals2
            ],
        },
        "test_eqg_3": {
            "test_equip_1": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals3
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals3
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals3
            ],
        },
    }
    return mock_site_emis


@pytest.fixture(name="mock_site_for_eqg_level_detect_emissions_testing")
def mock_site_for_eqg_level_detect_emissions_testing_fix(
    mocker, mock_site_emis_for_eqg_level_detect_emissions_testing
):
    mocker.patch.object(
        Site, "__init__", lambda self, *args, **kwargs: setattr(self, "_site_ID", 1)
    )
    mocker.patch.object(
        Site,
        "get_detectable_emissions",
        return_value=mock_site_emis_for_eqg_level_detect_emissions_testing,
    )
    expected_site_emis: float = (3 * 6) + (3 * 15) + (3 * 1.5)
    expected_eqg_survey_reports: list[EquipmentGroupSurveyReport] = [
        EquipmentGroupSurveyReport(1, "test_eqg_1", 18.0, 18.0),
        EquipmentGroupSurveyReport(1, "test_eqg_2", 45.0, 45.0),
        EquipmentGroupSurveyReport(1, "test_eqg_3", 4.5, 4.5),
    ]
    return (mocker, expected_site_emis, expected_eqg_survey_reports)


@pytest.fixture(name="mock_site_emis_for_eqg_level_detect_emissions_testing_lower_emis")
def mock_site_emis_for_eqg_level_detect_emissions_testing_lower_emis_fix(mocker):
    ret_vals: list[float] = [0.1, 0.15, 0.3]
    ret_vals2: list[float] = [0.2, 0.3, 0.1]
    ret_vals3: list[float] = [0.05, 0.01, 0.5]
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
                for retval in ret_vals2
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals2
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals2
            ],
        },
        "test_eqg_3": {
            "test_equip_1": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals3
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals3
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals3
            ],
        },
    }
    return mock_site_emis


@pytest.fixture(name="mock_site_for_eqg_level_detect_emissions_testing_lower_emissions")
def mock_site_for_eqg_level_detect_emissions_testing_lower_emissions_fix(
    mocker, mock_site_emis_for_eqg_level_detect_emissions_testing_lower_emis
) -> Tuple[Any, float, float]:
    mocker.patch.object(
        Site, "__init__", lambda self, *args, **kwargs: setattr(self, "_site_ID", 1)
    )
    mocker.patch.object(
        Site,
        "get_detectable_emissions",
        return_value=mock_site_emis_for_eqg_level_detect_emissions_testing_lower_emis,
    )
    expected_site_true_emis: float = (3 * 0.55) + (3 * 0.6) + (3 * 0.56)
    expected_site_measured_emis: float = 0.0
    expected_eqg_survey_reports: list[EquipmentGroupSurveyReport] = [
        EquipmentGroupSurveyReport(1, "test_eqg_1", 0, 1.65),
        EquipmentGroupSurveyReport(1, "test_eqg_2", 0, 1.8),
        EquipmentGroupSurveyReport(1, "test_eqg_3", 0, 1.68),
    ]
    return (
        mocker,
        expected_site_true_emis,
        expected_site_measured_emis,
        expected_eqg_survey_reports,
    )


@pytest.fixture(name="mock_site_emis_for_eqg_level_detect_emissions_testing_mixed_detect")
def mock_site_emis_for_eqg_level_detect_emissions_testing_mixed_detect_fix(mocker):
    ret_vals: list[float] = [0.1, 0.15, 0.3]
    ret_vals2: list[float] = [0.2, 0.3, 0.1]
    ret_vals3: list[float] = [0.5, 0.1, 0.5]
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
                for retval in ret_vals2
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals2
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals2
            ],
        },
        "test_eqg_3": {
            "test_equip_1": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals3
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals3
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals3
            ],
        },
    }
    return mock_site_emis


@pytest.fixture(name="mock_site_for_eqg_level_detect_emissions_testing_mixed_detect")
def mock_site_for_eqg_level_detect_emissions_testing_mixed_detect_fix(
    mocker, mock_site_emis_for_eqg_level_detect_emissions_testing_mixed_detect
) -> Tuple[Any, float, float]:
    mocker.patch.object(
        Site, "__init__", lambda self, *args, **kwargs: setattr(self, "_site_ID", 1)
    )
    mocker.patch.object(
        Site,
        "get_detectable_emissions",
        return_value=mock_site_emis_for_eqg_level_detect_emissions_testing_mixed_detect,
    )
    expected_site_true_emis: float = (3 * 0.55) + (3 * 0.6) + (3 * 1.1)
    expected_site_measured_emis: float = 3.3
    expected_eqg_survey_reports: list[EquipmentGroupSurveyReport] = [
        EquipmentGroupSurveyReport(1, "test_eqg_1", 0, 1.65),
        EquipmentGroupSurveyReport(1, "test_eqg_2", 0, 1.8),
        EquipmentGroupSurveyReport(1, "test_eqg_3", 3.3, 3.3),
    ]
    return (
        mocker,
        expected_site_true_emis,
        expected_site_measured_emis,
        expected_eqg_survey_reports,
    )
