from datetime import date
from typing import Tuple

import pandas as pd

from virtual_world import emission_types

from src.virtual_world.sources import Source
from src.file_processing.input_processing.emissions_source_processing import EmissionsSourceSample
from testing.unit_testing.test_virtual_world.test_sources.sources_testing_resources.sources_testing_fixtures import (  # noqa
    mock_source_and_params_for_create_emissions_rep_fix,
    mock_source_and_params_for_create_emissions_non_rep_fix,
    mock_simple_source_constructor_params_fix,
    create_emissions_data_non_persistent_fix,
    intermittent_source_params_fix,
    intermittent_source_params_non_rep_fix,
)
from testing.unit_testing.test_virtual_world.test_sources.sources_testing_resources import (  # noqa
    mock_methods,
)


def test_000_create_emission_creates_fugitive_emission_for_repairable_source(
    mock_source_and_params_for_create_emissions_rep: Tuple[Source, int, date, date],
) -> None:
    test_src: Source = mock_source_and_params_for_create_emissions_rep[0]
    leak_count, start_date, sim_start_date = mock_source_and_params_for_create_emissions_rep[1]
    emis: emission_types.Emission = test_src._create_emission(
        leak_count=leak_count,
        start_date=start_date,
        sim_start_date=sim_start_date,
        emission_rate_source_dictionary={
            "test": EmissionsSourceSample("test", "gram", "second", [1], 1000)
        },
        repair_delay_dataframe={},
    )
    assert emis is not None


def test_000_create_emission_creates_non_persistent_rep_emission_when_persistent_false(
    monkeypatch,
    create_emissions_data_non_persistent: Tuple[
        int, date, date, dict[str, EmissionsSourceSample], pd.DataFrame
    ],
    intermittent_source_params: dict[str, int],
) -> None:
    monkeypatch.setattr(
        Source, "__init__", mock_methods.mock_source_initialization_for_intermittent_source
    )
    test_source: Source = Source(**intermittent_source_params)
    created_emission: emission_types.Emission = test_source._create_emission(
        *create_emissions_data_non_persistent
    )
    assert created_emission is not None
    assert isinstance(created_emission, emission_types.IntermittentRepairableEmission)


def test_000_create_emission_creates_non_persistent_non_rep_emission_when_persistent_false(
    monkeypatch,
    create_emissions_data_non_persistent: Tuple[
        int, date, date, dict[str, EmissionsSourceSample], pd.DataFrame
    ],
    intermittent_source_params_non_rep: dict[str, int],
) -> None:
    monkeypatch.setattr(
        Source, "__init__", mock_methods.mock_source_initialization_for_intermittent_source
    )
    test_source: Source = Source(**intermittent_source_params_non_rep)
    created_emission: emission_types.Emission = test_source._create_emission(
        *create_emissions_data_non_persistent
    )
    assert created_emission is not None
    assert isinstance(created_emission, emission_types.IntermittentNonRepairableEmission)
