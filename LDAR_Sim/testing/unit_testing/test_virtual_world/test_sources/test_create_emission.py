from datetime import date
from typing import Tuple

from src.virtual_world.emissions import Emission
from src.virtual_world.sources import Source
from src.file_processing.input_processing.emissions_source_processing import EmissionsSourceSample
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
        leak_count=leak_count,
        start_date=start_date,
        sim_start_date=sim_start_date,
        emission_rate_source_dictionary={
            "test": EmissionsSourceSample("test", "gram", "second", [1], 1000)
        },
        repair_delay_dataframe={},
    )
    assert emis is not None
