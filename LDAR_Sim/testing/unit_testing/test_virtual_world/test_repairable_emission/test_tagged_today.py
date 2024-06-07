from virtual_world.emission_types.repairable_emission import RepairableEmission

from testing.unit_testing.test_virtual_world.test_repairable_emission.repairable_emission_testing_fixtures import (  # noqa
    mock_simple_fugitive_emission_for_tagged_today_testing_just_tagged_fix,
    mock_simple_fugitive_emission_for_tagged_today_testing_not_tagged_fix,
    mock_simple_fugitive_emission_for_tagged_today_testing_tagged_by_natural_fix,
    mock_simple_fugitive_emission_for_tagged_today_testing_tagged_previously_fix,
)


def test_000_tagged_today_returns_true_for_newly_tagged_by_test(
    mock_simple_fugitive_emission_for_tagged_today_testing_just_tagged: RepairableEmission,
) -> None:
    assert mock_simple_fugitive_emission_for_tagged_today_testing_just_tagged.tagged_today()


def test_000_tagged_today_returns_false_for_not_tagged(
    mock_simple_fugitive_emission_for_tagged_today_testing_not_tagged: RepairableEmission,
) -> None:
    assert not mock_simple_fugitive_emission_for_tagged_today_testing_not_tagged.tagged_today()


def test_000_tagged_today_returns_false_for_previously_tagged(
    mock_simple_fugitive_emission_for_tagged_today_testing_tagged_previously: RepairableEmission,
) -> None:
    assert (
        not mock_simple_fugitive_emission_for_tagged_today_testing_tagged_previously.tagged_today()
    )


def test_000_tagged_today_returns_false_for_tagged_by_natural(
    mock_simple_fugitive_emission_for_tagged_today_testing_tagged_by_natural: RepairableEmission,
) -> None:
    assert (
        not mock_simple_fugitive_emission_for_tagged_today_testing_tagged_by_natural.tagged_today()
    )
