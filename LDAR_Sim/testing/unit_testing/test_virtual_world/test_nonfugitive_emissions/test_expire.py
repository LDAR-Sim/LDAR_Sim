from datetime import date
from typing import Tuple
from testing.unit_testing.test_virtual_world.test_nonfugitive_emissions.nonfugitive_emission_testing_fixtures import (  # noqa
    mock_simple_nonfugitive_emission_for_expire_testing_1_fix,
)
from src.constants.general_const import Emission_Constants as ec
from src.virtual_world.nonfugitive_emissions import NonRepairableEmission
from src.file_processing.output_processing.output_utils import EmisInfo


def test_000_expire_applies_correctly_to_simple_case(
    mock_simple_nonfugitive_emission_for_expire_testing_1: Tuple[NonRepairableEmission, date],
):
    emis: EmisInfo = EmisInfo()
    mock_simple_nonfugitive_emission_for_expire_testing_1[0].expire(emis)
    assert mock_simple_nonfugitive_emission_for_expire_testing_1[0]._record is False
    assert (
        mock_simple_nonfugitive_emission_for_expire_testing_1[0]._recorded_by_company == ec.EXPIRE
    )
    assert mock_simple_nonfugitive_emission_for_expire_testing_1[0]._status == ec.EXPIRE
    assert (
        mock_simple_nonfugitive_emission_for_expire_testing_1[0]._expiry_date
        == mock_simple_nonfugitive_emission_for_expire_testing_1[1]
    )
