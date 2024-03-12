from datetime import date
from typing import Tuple
from src.virtual_world.nonfugitive_emissions import NonRepairableEmission

from testing.unit_testing.test_virtual_world.test_nonfugitive_emissions.nonfugitive_emission_testing_fixtures import (  # noqa
    mock_simple_nonfugitive_emission_for_record_testing_1_fix,
    mock_simple_nonfugitive_emission_for_record_testing_already_recorded_fix,
)


def test_000_record_correctly_sets_record_to_true(
    mock_simple_nonfugitive_emission_for_record_testing_1: Tuple[
        NonRepairableEmission, Tuple[float, date, int, str, str, int]
    ],
) -> None:
    nonrep_emis: NonRepairableEmission = mock_simple_nonfugitive_emission_for_record_testing_1[0]
    (
        measured_rate,
        cur_date,
        t_since_ldar,
        company,
        crew_id,
    ) = mock_simple_nonfugitive_emission_for_record_testing_1[1]
    nonrep_emis.record_emission(measured_rate, cur_date, t_since_ldar, company, crew_id)
    assert nonrep_emis._record is True


def test_000_record_correctly_returns_false_with_no_overwrite_when_already_recorded(
    mock_simple_nonfugitive_emission_for_record_testing_already_recorded: Tuple[
        NonRepairableEmission, Tuple[float, date, int, str, str, int]
    ],
) -> None:
    nonrep_emis: NonRepairableEmission = (
        mock_simple_nonfugitive_emission_for_record_testing_already_recorded[0]
    )
    (
        measured_rate,
        cur_date,
        t_since_ldar,
        company,
        crew_id,
    ) = mock_simple_nonfugitive_emission_for_record_testing_already_recorded[1]
    new_leak = nonrep_emis.record_emission(measured_rate, cur_date, t_since_ldar, company, crew_id)
    assert not new_leak


def test_000_record_correctly_sets_input_args(
    mock_simple_nonfugitive_emission_for_record_testing_1: Tuple[
        NonRepairableEmission, Tuple[float, date, int, str, str, int]
    ],
) -> None:
    nonrep_emis: NonRepairableEmission = mock_simple_nonfugitive_emission_for_record_testing_1[0]
    (
        measured_rate,
        cur_date,
        t_since_ldar,
        company,
        crew_id,
    ) = mock_simple_nonfugitive_emission_for_record_testing_1[1]
    nonrep_emis.record_emission(measured_rate, cur_date, t_since_ldar, company, crew_id)
    assert nonrep_emis._measured_rate == measured_rate
    assert nonrep_emis._recorded_by_company == company
    assert nonrep_emis._recorded_by_crew == crew_id


def test_000_record_correctly_calls_estimate_start_days(
    mocker,
    mock_simple_nonfugitive_emission_for_record_testing_1: Tuple[
        NonRepairableEmission, Tuple[float, date, int, str, str, int]
    ],
) -> None:
    nonrep_emis: NonRepairableEmission = mock_simple_nonfugitive_emission_for_record_testing_1[0]
    mocker.patch.object(nonrep_emis, "estimate_start_date")
    (
        measured_rate,
        cur_date,
        t_since_ldar,
        company,
        crew_id,
    ) = mock_simple_nonfugitive_emission_for_record_testing_1[1]
    nonrep_emis.record_emission(measured_rate, cur_date, t_since_ldar, company, crew_id)
    nonrep_emis.estimate_start_date.assert_called_once()


def test_000_record_returns_true_for_new_record(
    mock_simple_nonfugitive_emission_for_record_testing_1: Tuple[
        NonRepairableEmission, Tuple[float, date, int, str, str, int]
    ],
) -> None:
    nonrep_emis: NonRepairableEmission = mock_simple_nonfugitive_emission_for_record_testing_1[0]
    (
        measured_rate,
        cur_date,
        t_since_ldar,
        company,
        crew_id,
    ) = mock_simple_nonfugitive_emission_for_record_testing_1[1]
    new_leak = nonrep_emis.record_emission(measured_rate, cur_date, t_since_ldar, company, crew_id)
    assert new_leak
