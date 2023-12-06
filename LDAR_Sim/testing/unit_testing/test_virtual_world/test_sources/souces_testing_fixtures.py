from datetime import datetime
from typing import Tuple
import pytest

from virtual_world.sources import Source
from virtual_world.infrastructure_const import Infrastructure_Constants


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
        Infrastructure_Constants.Sources_File_Constants.REPAIR_DELAY: 14,
        Infrastructure_Constants.Sources_File_Constants.REPAIR_COST: 200,
        "Method_Specific_Params": {
            Infrastructure_Constants.Sources_File_Constants.SPATIAL_PLACEHOLDER: {}
        },
    }
    return (src_id, src_info, prop_params)


@pytest.fixture(name="mock_source_and_params_for_create_emissions_rep")
def mock_source_and_params_for_create_emissions_rep_fix(
    mock_simple_source_constructor_params: Tuple[str, dict, dict]
) -> tuple[Source, int, datetime, datetime]:
    src_id, src_info, prop_param = mock_simple_source_constructor_params
    test_source: Source = Source(src_id, src_info, prop_param)
    emission_parameters: Tuple[int, datetime, datetime] = (
        1,
        datetime(*[2023, 1, 1]),
        datetime(*[2023, 1, 1]),
    )
    return (test_source, emission_parameters)


@pytest.fixture(name="mock_source_and_params_for_create_emissions_non_rep")
def mock_source_and_params_for_create_emissions_non_rep_fix(
    mock_simple_source_constructor_params: Tuple[str, dict, dict]
) -> tuple[Source, int, datetime, datetime]:
    src_id, src_info, prop_param = mock_simple_source_constructor_params
    src_info[Infrastructure_Constants.Sources_File_Constants.REPAIRABLE] = False
    test_source: Source = Source(src_id, src_info, prop_param)
    emission_parameters: Tuple[int, datetime, datetime] = (
        1,
        datetime(*[2023, 1, 1]),
        datetime(*[2023, 1, 1]),
    )
    return (test_source, emission_parameters)
