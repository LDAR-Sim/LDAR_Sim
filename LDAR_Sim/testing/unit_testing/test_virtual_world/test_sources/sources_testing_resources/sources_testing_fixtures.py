from datetime import date
from typing import Tuple
import pandas as pd
import pytest

from file_processing.input_processing.emissions_source_processing import EmissionsSourceSample
from src.virtual_world.sources import Source
from src.constants.infrastructure_const import Infrastructure_Constants
from src.constants.param_default_const import Common_Params as cp


@pytest.fixture(name="mock_simple_source_constructor_params")
def mock_simple_source_constructor_params_fix() -> Tuple[str, dict, dict]:
    src_id: str = "test"
    src_info: dict = {
        Infrastructure_Constants.Sources_File_Constants.REPAIRABLE: True,
        Infrastructure_Constants.Sources_File_Constants.PERSISTENT: True,
        Infrastructure_Constants.Sources_File_Constants.ACTIVE_DUR: 1,
        Infrastructure_Constants.Sources_File_Constants.INACTIVE_DUR: 0,
    }
    prop_params: dict = {
        Infrastructure_Constants.Sources_File_Constants.EMIS_ERS: "test",
        Infrastructure_Constants.Sources_File_Constants.EMIS_EPR: 1,
        Infrastructure_Constants.Sources_File_Constants.EMIS_DUR: 1,
        Infrastructure_Constants.Sources_File_Constants.MULTI_EMISSIONS: False,
        Infrastructure_Constants.Sources_File_Constants.REPAIR_DELAY: {cp.VAL: [14]},
        Infrastructure_Constants.Sources_File_Constants.REPAIR_COST: {cp.VAL: [200]},
        cp.METH_SPECIFIC: {Infrastructure_Constants.Sources_File_Constants.SPATIAL_PLACEHOLDER: {}},
    }
    return (src_id, src_info, prop_params)


@pytest.fixture(name="mock_source_and_params_for_create_emissions_rep")
def mock_source_and_params_for_create_emissions_rep_fix(
    mock_simple_source_constructor_params: Tuple[str, dict, dict]
) -> tuple[Source, int, date, date]:
    src_id, src_info, prop_param = mock_simple_source_constructor_params
    test_source: Source = Source(src_id, src_info, prop_param)
    emission_parameters: Tuple[int, date, date] = (
        1,
        date(*[2023, 1, 1]),
        date(*[2023, 1, 1]),
    )
    return (test_source, emission_parameters)


@pytest.fixture(name="mock_source_and_params_for_create_emissions_non_rep")
def mock_source_and_params_for_create_emissions_non_rep_fix(
    mock_simple_source_constructor_params: Tuple[str, dict, dict]
) -> tuple[Source, int, date, date]:
    src_id, src_info, prop_param = mock_simple_source_constructor_params
    src_info[Infrastructure_Constants.Sources_File_Constants.REPAIRABLE] = False
    test_source: Source = Source(src_id, src_info, prop_param)
    emission_parameters: Tuple[int, date, date] = (
        1,
        date(*[2023, 1, 1]),
        date(*[2023, 1, 1]),
    )
    return (test_source, emission_parameters)


@pytest.fixture(name="mock_source_and_args_for_generate_emissions")
def mock_source_and_args_for_generate_emissions_fix(
    mock_simple_source_constructor_params: Tuple[str, dict, dict]
) -> tuple[Source, int, date, date]:
    src_id, src_info, prop_param = mock_simple_source_constructor_params
    prop_param[Infrastructure_Constants.Sources_File_Constants.EMIS_EPR] = 0.0065
    test_source: Source = Source(src_id, src_info, prop_param)
    sim_sd = date(*[2023, 1, 1])
    sim_ed = date(*[2027, 12, 31])
    n_sims = 1000
    expected_avg_res = 11.86
    return (test_source, (sim_sd, sim_ed, n_sims), expected_avg_res)


@pytest.fixture(name="mock_source_and_args_for_generate_emissions_same_st_ed")
def mock_source_and_args_for_generate_emissions_same_st_ed_fix(
    mock_simple_source_constructor_params: Tuple[str, dict, dict]
) -> tuple[Source, int, date, date]:
    src_id, src_info, prop_param = mock_simple_source_constructor_params
    prop_param[Infrastructure_Constants.Sources_File_Constants.EMIS_EPR] = 0.0065
    test_source: Source = Source(src_id, src_info, prop_param)
    sim_sd = date(*[2023, 1, 1])
    sim_ed = date(*[2023, 1, 1])
    n_sims = 2000
    expected_avg_res = 0.0065
    return (test_source, (sim_sd, sim_ed, n_sims), expected_avg_res)


@pytest.fixture(name="create_emissions_data_non_persistent")
def create_emissions_data_non_persistent_fix() -> (
    Tuple[Tuple[int, date, date, dict[str, EmissionsSourceSample], pd.DataFrame], Tuple[int, int]]
):
    return (
        1,
        date(*[2023, 1, 1]),
        date(*[2023, 1, 1]),
        {"test": EmissionsSourceSample("test", "gram", "second", [1], 1000)},
        pd.DataFrame(),
    )


@pytest.fixture(name="intermittent_source_params")
def intermittent_source_params_fix() -> dict[str, int]:
    return {
        "active_duration": 90,
        "inactive_duration": 90,
    }


@pytest.fixture(name="intermittent_source_params_non_rep")
def intermittent_source_params_non_rep_fix() -> dict[str, int]:
    return {
        "active_duration": 90,
        "inactive_duration": 90,
        "repairable": False,
    }
