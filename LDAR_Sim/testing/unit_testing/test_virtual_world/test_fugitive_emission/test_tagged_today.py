from virtual_world.fugitive_emission import FugitiveEmission

from testing.unit_testing.test_virtual_world.test_fugitive_emission.fugitive_emission_testing_fixtures import (  # noqa
    mock_simple_fugitive_emission_for_tagged_today_testing_just_tagged_fix,
    mock_simple_fugitive_emission_for_tagged_today_testing_not_tagged_fix,
    mock_simple_fugitive_emission_for_tagged_today_testing_tagged_by_natural_fix,
    mock_simple_fugitive_emission_for_tagged_today_testing_tagged_previously_fix,
)


def test_000_tagged_today_returns_true_for_newly_tagged_by_test(
    mock_simple_fugitive_emission_for_tagged_today_testing_just_tagged: FugitiveEmission,
) -> None:
    assert mock_simple_fugitive_emission_for_tagged_today_testing_just_tagged.tagged_today()


def test_000_tagged_today_returns_false_for_not_tagged(
    mock_simple_fugitive_emission_for_tagged_today_testing_not_tagged: FugitiveEmission,
) -> None:
    assert not mock_simple_fugitive_emission_for_tagged_today_testing_not_tagged.tagged_today()


def test_000_tagged_today_returns_false_for_previously_tagged(
    mock_simple_fugitive_emission_for_tagged_today_testing_tagged_previously: FugitiveEmission,
) -> None:
    assert (
        not mock_simple_fugitive_emission_for_tagged_today_testing_tagged_previously.tagged_today()
    )


def test_000_tagged_today_returns_false_for_tagged_by_natural(
    mock_simple_fugitive_emission_for_tagged_today_testing_tagged_by_natural: FugitiveEmission,
) -> None:
    assert (
        not mock_simple_fugitive_emission_for_tagged_today_testing_tagged_by_natural.tagged_today()
    )
