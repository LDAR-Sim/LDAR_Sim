from datetime import date
from typing import Tuple
from virtual_world.emission_types.repairable_emission import RepairableEmission

from testing.unit_testing.test_virtual_world.test_repairable_emission.repairable_emission_testing_fixtures import (  # noqa
    mock_simple_fugitive_emission_for_tag_leak_testing_1_fix,
    mock_simple_fugitive_emission_for_tag_leak_testing_already_tagged_fix,
)


def test_000_tag_leak_correctly_sets_tagged_to_true(
    mock_simple_fugitive_emission_for_tag_leak_testing_1: Tuple[
        RepairableEmission, Tuple[float, date, int, str, str, int]
    ],
) -> None:
    fug_emis: RepairableEmission = mock_simple_fugitive_emission_for_tag_leak_testing_1[0]
    (
        measured_rate,
        cur_date,
        t_since_ldar,
        company,
        crew_id,
        tagging_rep_delay,
    ) = mock_simple_fugitive_emission_for_tag_leak_testing_1[1]
    fug_emis.tag_leak(measured_rate, cur_date, t_since_ldar, company, crew_id, tagging_rep_delay)
    assert fug_emis._tagged is True


def test_000_tag_leak_correctly_returns_false__with_no_overwrite_when_already_tagged(
    mock_simple_fugitive_emission_for_tag_leak_testing_already_tagged: Tuple[
        RepairableEmission, Tuple[float, date, int, str, str, int]
    ],
) -> None:
    fug_emis: RepairableEmission = (
        mock_simple_fugitive_emission_for_tag_leak_testing_already_tagged[0]
    )
    (
        measured_rate,
        cur_date,
        t_since_ldar,
        company,
        crew_id,
        tagging_rep_delay,
    ) = mock_simple_fugitive_emission_for_tag_leak_testing_already_tagged[1]
    new_leak = fug_emis.tag_leak(
        measured_rate, cur_date, t_since_ldar, company, crew_id, tagging_rep_delay
    )
    assert not new_leak


def test_000_tag_leak_correctly_sets_input_args(
    mock_simple_fugitive_emission_for_tag_leak_testing_1: Tuple[
        RepairableEmission, Tuple[float, date, int, str, str, int]
    ],
) -> None:
    fug_emis: RepairableEmission = mock_simple_fugitive_emission_for_tag_leak_testing_1[0]
    (
        measured_rate,
        cur_date,
        t_since_ldar,
        company,
        crew_id,
        tagging_rep_delay,
    ) = mock_simple_fugitive_emission_for_tag_leak_testing_1[1]
    fug_emis.tag_leak(measured_rate, cur_date, t_since_ldar, company, crew_id, tagging_rep_delay)
    assert fug_emis._measured_rate == measured_rate
    assert fug_emis._tagged_by_company == company
    assert fug_emis._tagged_by_crew == crew_id
    assert fug_emis._tagging_rep_delay == tagging_rep_delay


def test_000_tag_leak_correctly_calls_estimate_start_days(
    mocker,
    mock_simple_fugitive_emission_for_tag_leak_testing_1: Tuple[
        RepairableEmission, Tuple[float, date, int, str, str, int]
    ],
) -> None:
    fug_emis: RepairableEmission = mock_simple_fugitive_emission_for_tag_leak_testing_1[0]
    mocker.patch.object(fug_emis, "estimate_start_date")
    (
        measured_rate,
        cur_date,
        t_since_ldar,
        company,
        crew_id,
        tagging_rep_delay,
    ) = mock_simple_fugitive_emission_for_tag_leak_testing_1[1]
    fug_emis.tag_leak(measured_rate, cur_date, t_since_ldar, company, crew_id, tagging_rep_delay)
    fug_emis.estimate_start_date.assert_called_once()


def test_000_tag_leak_returns_true_for_new_tag(
    mock_simple_fugitive_emission_for_tag_leak_testing_1: Tuple[
        RepairableEmission, Tuple[float, date, int, str, str, int]
    ],
) -> None:
    fug_emis: RepairableEmission = mock_simple_fugitive_emission_for_tag_leak_testing_1[0]
    (
        measured_rate,
        cur_date,
        t_since_ldar,
        company,
        crew_id,
        tagging_rep_delay,
    ) = mock_simple_fugitive_emission_for_tag_leak_testing_1[1]
    new_leak = fug_emis.tag_leak(
        measured_rate, cur_date, t_since_ldar, company, crew_id, tagging_rep_delay
    )
    assert new_leak
