from typing import Any, Tuple
import pytest
from src.scheduling.schedule_dataclasses import (
    EquipmentGroupSurveyReport,
    EmissionDetectionReport,
)
from src.virtual_world.emissions import Emission

from src.virtual_world.sites import Site


@pytest.fixture(name="sensor_info_for_default_equipment_level_sensor_construction_testing")
def sensor_info_for_default_equipment_level_sensor_construction_testing_fix() -> dict[str, int]:
    return {"mdl": [1], "QE": 0.0}


@pytest.fixture(name="sensor_info_high_mdl_for_default_equipment_level_sensor_testing")
def sensor_info_high_mdl_for_default_equipment_level_sensor_testing_fix() -> dict[str, int]:
    return {"mdl": [2.0], "QE": 0.0}


@pytest.fixture(name="mock_site_emis_for_equip_level_detect_emissions_testing")
def mock_site_emis_for_equip_level_detect_emissions_testing_fix(mocker):
    ret_vals: list[float] = [1.0, 2.0, 3.0]
    ret_vals2: list[float] = [4.0, 5.0, 6.0]
    ret_vals3: list[float] = [7.0, 8.0, 9.0]
    ret_vals4: list[float] = [1.1, 2.1, 3.1]
    ret_vals5: list[float] = [4.1, 5.1, 6.1]
    ret_vals6: list[float] = [7.1, 8.1, 9.1]
    ret_vals7: list[float] = [1.2, 2.2, 3.2]
    ret_vals8: list[float] = [4.2, 5.2, 6.2]
    ret_vals9: list[float] = [7.2, 8.2, 9.2]
    mock_site_emis: dict[str, dict[str, list[Emission]]] = {
        "test_eqg_1": {
            "test_equip_1": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals2
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals3
            ],
        },
        "test_eqg_2": {
            "test_equip_1": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals4
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals5
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals6
            ],
        },
        "test_eqg_3": {
            "test_equip_1": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals7
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals8
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals9
            ],
        },
    }
    return mock_site_emis


@pytest.fixture(name="mock_site_for_equip_level_detect_emissions_testing")
def mock_site_for_equip_level_detect_emissions_testing_fix(
    mocker, mock_site_emis_for_equip_level_detect_emissions_testing
):
    mocker.patch.object(
        Site, "__init__", lambda self, *args, **kwargs: setattr(self, "_site_ID", 1)
    )
    mocker.patch.object(
        Site,
        "get_detectable_emissions",
        return_value=mock_site_emis_for_equip_level_detect_emissions_testing,
    )
    expected_site_emis: float = (45) + (45.9) + (46.8)
    expected_eqg_survey_reports: list[EquipmentGroupSurveyReport] = [
        EquipmentGroupSurveyReport(
            1,
            "test_eqg_1",
            45.0,
            45.0,
            emissions_detected=[
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_1", 6.0, 6.0),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_2", 15.0, 15.0),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_3", 24.0, 24.0),
            ],
        ),
        EquipmentGroupSurveyReport(
            1,
            "test_eqg_2",
            45.9,
            45.9,
            emissions_detected=[
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_1", 6.3, 6.3),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_2", 15.3, 15.3),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_3", 24.3, 24.3),
            ],
        ),
        EquipmentGroupSurveyReport(
            1,
            "test_eqg_3",
            46.8,
            46.8,
            emissions_detected=[
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_1", 6.6, 6.6),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_2", 15.6, 15.6),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_3", 24.6, 24.6),
            ],
        ),
    ]
    return (mocker, expected_site_emis, expected_eqg_survey_reports)


@pytest.fixture(name="mock_site_emis_for_equip_level_detect_emissions_testing_lower_emis")
def mock_site_emis_for_equip_level_detect_emissions_testing_lower_emis_fix(mocker):
    ret_vals: list[float] = [0.3, 0.3, 0.3]
    ret_vals2: list[float] = [0.2, 0.2, 0.2]
    ret_vals3: list[float] = [0.1, 0.1, 0.1]
    ret_vals4: list[float] = [0.25, 0.25, 0.25]
    ret_vals5: list[float] = [0.15, 0.15, 0.15]
    ret_vals6: list[float] = [0.05, 0.05, 0.05]
    ret_vals7: list[float] = [0.1, 0.2, 0.3]
    ret_vals8: list[float] = [0.2, 0.5, 0.05]
    ret_vals9: list[float] = [0.1, 0.15, 0.25]
    mock_site_emis: dict[str, dict[str, list[Emission]]] = {
        "test_eqg_1": {
            "test_equip_1": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals2
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals3
            ],
        },
        "test_eqg_2": {
            "test_equip_1": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals4
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals5
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals6
            ],
        },
        "test_eqg_3": {
            "test_equip_1": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals7
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals8
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals9
            ],
        },
    }
    return mock_site_emis


@pytest.fixture(name="mock_site_for_equip_level_detect_emissions_testing_lower_emissions")
def mock_site_for_equip_level_detect_emissions_testing_lower_emissions_fix(
    mocker, mock_site_emis_for_equip_level_detect_emissions_testing_lower_emis
) -> Tuple[Any, float, float]:
    mocker.patch.object(
        Site, "__init__", lambda self, *args, **kwargs: setattr(self, "_site_ID", 1)
    )
    mocker.patch.object(
        Site,
        "get_detectable_emissions",
        return_value=mock_site_emis_for_equip_level_detect_emissions_testing_lower_emis,
    )
    expected_site_true_emis: float = (0.9 + 0.6 + 0.3) + (0.75 + 0.45 + 0.15) + (0.6 + 0.75 + 0.5)
    expected_site_measured_emis: float = 0.0
    expected_eqg_survey_reports: list[EquipmentGroupSurveyReport] = [
        EquipmentGroupSurveyReport(
            1,
            "test_eqg_1",
            0.0,
            (0.9 + 0.6 + 0.3),
            emissions_detected=[
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_1", 0, 0.9),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_2", 0, 0.6),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_3", 0, 0.3),
            ],
        ),
        EquipmentGroupSurveyReport(
            1,
            "test_eqg_2",
            0.0,
            (0.75 + 0.45 + 0.15),
            emissions_detected=[
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_1", 0, 0.75),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_2", 0, 0.45),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_3", 0, 0.15),
            ],
        ),
        EquipmentGroupSurveyReport(
            1,
            "test_eqg_3",
            0.0,
            (0.6 + 0.75 + 0.5),
            emissions_detected=[
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_1", 0, 0.6),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_2", 0, 0.75),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_3", 0, 0.5),
            ],
        ),
    ]
    return (
        mocker,
        expected_site_true_emis,
        expected_site_measured_emis,
        expected_eqg_survey_reports,
    )


@pytest.fixture(name="mock_site_emis_for_equip_level_detect_emissions_testing_mixed_detect")
def mock_site_emis_for_equip_level_detect_emissions_testing_mixed_detect_fix(mocker):
    ret_vals: list[float] = [1.0, 2.0, 3.0]
    ret_vals2: list[float] = [4.0, 5.0, 6.0]
    ret_vals3: list[float] = [7.0, 8.0, 9.0]
    ret_vals4: list[float] = [0.25, 0.25, 0.25]
    ret_vals5: list[float] = [0.15, 0.15, 0.15]
    ret_vals6: list[float] = [0.05, 0.05, 0.05]
    ret_vals7: list[float] = [1.2, 2.2, 3.2]
    ret_vals8: list[float] = [4.2, 5.2, 6.2]
    ret_vals9: list[float] = [7.2, 8.2, 9.2]
    mock_site_emis: dict[str, dict[str, list[Emission]]] = {
        "test_eqg_1": {
            "test_equip_1": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals2
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals3
            ],
        },
        "test_eqg_2": {
            "test_equip_1": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals4
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals5
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals6
            ],
        },
        "test_eqg_3": {
            "test_equip_1": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals7
            ],
            "test_equip_2": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals8
            ],
            "test_equip_3": [
                mocker.MagicMock(Emission, get_rate=mocker.MagicMock(return_value=retval))
                for retval in ret_vals9
            ],
        },
    }
    return mock_site_emis


@pytest.fixture(name="mock_site_for_equip_level_detect_emissions_testing_mixed_detect")
def mock_site_for_equip_level_detect_emissions_testing_mixed_detect_fix(
    mocker, mock_site_emis_for_equip_level_detect_emissions_testing_mixed_detect
) -> Tuple[Any, float, float]:
    mocker.patch.object(
        Site, "__init__", lambda self, *args, **kwargs: setattr(self, "_site_ID", 1)
    )
    mocker.patch.object(
        Site,
        "get_detectable_emissions",
        return_value=mock_site_emis_for_equip_level_detect_emissions_testing_mixed_detect,
    )
    expected_site_true_emis: float = (45) + (0.75 + 0.45 + 0.15) + (46.8)
    expected_site_measured_emis: float = 45 + 46.8
    expected_eqg_survey_reports: list[EquipmentGroupSurveyReport] = [
        EquipmentGroupSurveyReport(
            1,
            "test_eqg_1",
            45.0,
            45.0,
            emissions_detected=[
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_1", 6.0, 6.0),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_2", 15.0, 15.0),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_3", 24.0, 24.0),
            ],
        ),
        EquipmentGroupSurveyReport(
            1,
            "test_eqg_2",
            0.0,
            (0.75 + 0.45 + 0.15),
            emissions_detected=[
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_1", 0, 0.75),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_2", 0, 0.45),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_3", 0, 0.15),
            ],
        ),
        EquipmentGroupSurveyReport(
            1,
            "test_eqg_3",
            46.8,
            46.8,
            emissions_detected=[
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_1", 6.6, 6.6),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_2", 15.6, 15.6),
                EmissionDetectionReport(1, "test_eqg_1", "test_equip_3", 24.6, 24.6),
            ],
        ),
    ]
    return (
        mocker,
        expected_site_true_emis,
        expected_site_measured_emis,
        expected_eqg_survey_reports,
    )
