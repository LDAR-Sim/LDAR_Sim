import copy
from datetime import date
from virtual_world import emission_types
from testing.unit_testing.test_virtual_world.test_non_repairable_emission.non_repairable_emission_testing_fixtures import (  # noqa
    mock_nonfugitive_emission_for_update_detection_records_no_prior_detection_fix,
    mock_nonfugitive_emission_for_update_detection_records_w_prior_detection_fix,
)


def test_000_update_detection_records_correctly_sets_detection_info_where_no_prior_detection(
    mock_nonfugitive_emission_for_update_detection_records_no_prior_detection: (
        emission_types.NonRepairableEmission
    ),
) -> None:
    detec_company = "Testing"
    detec_date = date(*[2020, 1, 1])
    (
        mock_nonfugitive_emission_for_update_detection_records_no_prior_detection
    ).update_detection_records(detec_company, detec_date)
    assert (
        mock_nonfugitive_emission_for_update_detection_records_no_prior_detection._init_detect_by
        == detec_company
    )
    assert (
        mock_nonfugitive_emission_for_update_detection_records_no_prior_detection._init_detect_date
        == detec_date
    )


def test_000_update_detection_records_does_not_overwrite_prior_detection_record_if_existing(
    mock_nonfugitive_emission_for_update_detection_records_w_prior_detection: (
        emission_types.NonRepairableEmission
    ),
) -> None:
    prev_detect_company = copy.deepcopy(
        mock_nonfugitive_emission_for_update_detection_records_w_prior_detection._init_detect_by
    )
    prev_detect_date = copy.deepcopy(
        mock_nonfugitive_emission_for_update_detection_records_w_prior_detection._init_detect_date
    )
    detec_company = "Testing"
    detec_date = date(*[2020, 1, 1])
    (
        mock_nonfugitive_emission_for_update_detection_records_w_prior_detection
    ).update_detection_records(detec_company, detec_date)
    assert (
        mock_nonfugitive_emission_for_update_detection_records_w_prior_detection._init_detect_by
        == prev_detect_company
    )
    assert (
        mock_nonfugitive_emission_for_update_detection_records_w_prior_detection._init_detect_date
        == prev_detect_date
    )
