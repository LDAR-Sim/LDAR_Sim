from datetime import date
from typing import Tuple

import pytest
from virtual_world.emissions import Emission
from virtual_world.sources import Source

from testing.unit_testing.test_virtual_world.test_sources.sources_testing_fixtures import (  # noqa
    mock_source_and_params_for_create_emissions_rep_fix,
    mock_source_and_params_for_create_emissions_non_rep_fix,
    mock_simple_source_constructor_params_fix,
)


def test_000_create_emission_creates_fugitive_emission_for_repairable_source(
    mock_source_and_params_for_create_emissions_rep: Tuple[Source, int, date, date],
) -> None:
    test_src: Source = mock_source_and_params_for_create_emissions_rep[0]
    leak_count, start_date, sim_start_date = mock_source_and_params_for_create_emissions_rep[1]
    emis: Emission = test_src._create_emission(
        leak_count=leak_count, start_date=start_date, sim_start_date=sim_start_date
    )
    assert emis is not None


def test_000_create_emission_returns_WIP_feature_message_for_non_repairable_sources(
    capsys: pytest.CaptureFixture[str],
    mock_source_and_params_for_create_emissions_non_rep: Tuple[Source, int, date, date],
) -> None:
    test_src: Source = mock_source_and_params_for_create_emissions_non_rep[0]
    leak_count, start_date, sim_start_date = mock_source_and_params_for_create_emissions_non_rep[1]
    with pytest.raises(SystemExit) as e:
        test_src._create_emission(
            leak_count=leak_count, start_date=start_date, sim_start_date=sim_start_date
        )
    err_msg = capsys.readouterr()
    assert Source.WIP_NON_FUG_EMIS_GENERATION_MSG in err_msg.out
    assert e.value.code is None
