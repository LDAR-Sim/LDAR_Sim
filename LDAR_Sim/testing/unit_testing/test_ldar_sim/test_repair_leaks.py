""" Module for testing the ldar_sim.py function repair_leaks"""
from src.ldar_sim import LdarSim

import datetime

from testing.unit_testing.test_ldar_sim.ldar_sim_testing_fixtures \
    import (  # Noqa: 401
        mock_state_for_ldar_sim_testing_1_fix,
        mock_program_params_for_ldar_sim_testing_1_fix,
        mock_vw_for_ldar_sim_testing_1_fix,
        mock_timeseries_for_ldar_sim_testing_1_fix,
        mock_vw_for_ldar_sim_testing_2_fix,
        mock_state_for_ldar_sim_testing_2_fix,
        mock_program_params_for_ldar_sim_testing_2_fix,
        mock_sim_settings_for_ldar_sim_testing_2_fix
    )


def test_001_natural_repair_adds_to_natural_repair_cost(
        mock_state_for_ldar_sim_testing_1,
        mock_program_params_for_ldar_sim_testing_1,
        mock_vw_for_ldar_sim_testing_1,
        mock_timeseries_for_ldar_sim_testing_1
):
    ldarsim = LdarSim(
        None,
        mock_state_for_ldar_sim_testing_1,
        mock_program_params_for_ldar_sim_testing_1,
        mock_vw_for_ldar_sim_testing_1,
        mock_timeseries_for_ldar_sim_testing_1,
        None,
        None
    )
    ldarsim.state['sites'][0]['active_leaks'][0]['date_tagged'] = datetime.datetime(
        2017, 1, 1, 8, 0)
    ldarsim.repair_leaks()
    assert ldarsim.timeseries['repair_cost'][1] == 0
    assert ldarsim.timeseries['nat_repair_cost'][1] == 200
    assert ldarsim.timeseries['verification_cost'][1] == 0


def test_001_non_natural_repair_adds_to_repair_cost(
        mock_sim_settings_for_ldar_sim_testing_2,
        mock_state_for_ldar_sim_testing_2,
        mock_program_params_for_ldar_sim_testing_2,
        mock_vw_for_ldar_sim_testing_2,
        mock_timeseries_for_ldar_sim_testing_1
):
    ldarsim = LdarSim(
        mock_sim_settings_for_ldar_sim_testing_2,
        mock_state_for_ldar_sim_testing_2,
        mock_program_params_for_ldar_sim_testing_2,
        mock_vw_for_ldar_sim_testing_2,
        mock_timeseries_for_ldar_sim_testing_1,
        None,
        None
    )
    ldarsim.state['sites'][0]['active_leaks'][0]['date_tagged'] = datetime.datetime(
        2017, 1, 1, 8, 0)
    ldarsim.repair_leaks()
    assert ldarsim.timeseries['repair_cost'][1] == 200
    assert ldarsim.timeseries['nat_repair_cost'][1] == 0
    assert ldarsim.timeseries['verification_cost'][1] == 100
