"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:   file_name_constats.py
Purpose: Contains constants used to define file names

This program is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published
by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
MIT License for more details.
You should have received a copy of the MIT License
along with this program.  If not, see <https://opensource.org/licenses/MIT>.

------------------------------------------------------------------------------
"""

from dataclasses import dataclass


@dataclass
class Default_Files:
    VIRTUAL_DEF_FILE = "virtual_world_default.yml"
    SIM_SETTING_DEF_FILE = "simulation_settings_default.yml"
    PROG_DEF_FILE = "p_default.yml"
    METH_STATIONARY_DEF_FILE = "m_default_stationary.yml"
    METH_MOBILE_DEF_FILE = "m_default_mobile.yml"
    OUTPUT_DEF_FILE = "outputs_default.yml"


@dataclass
class Generator_Files:
    PRESEED_FILE = "preseed.p"
    EMISSION_PRESEED_FILE = "emis_preseed.p"
    N_SIM_SAVE_FILE = "n_sim_saved.p"

    HASH_FILE = "gen_infrastructure_hashes.p"
    INFRA_FILE = "gen_infrastructure.p"

    GENERATOR_FOLDER = "generator"

    GEN_INFRA_EMISS = "gen_infrastructure_emissions_{i}.p"


@dataclass
class Output_Files:
    @dataclass
    class SummaryFileNames:
        TS_SUMMARY = "Timeseries Summary"
        EMIS_SUMMARY = "Emissions Summary"
        EMIS_EST_SUMMARY = "Estimated Emissions Summary"
        EMIS_FUG_EST_SUMMARY = "Estimated Fugitive Emissions Summary"

        def __iter__(self):
            for attr_name, attr_value in vars(self.__class__).items():
                if not callable(attr_value) and not attr_name.startswith("__"):
                    yield attr_value

    TRUE_VS_ESTIMATED_PERCENT_DIFF_PLOT = "True_vs_Estimated_Emissions_percent_differences.png"
    TRUE_VS_ESTIMATED_RELATIVE_DIFF_PLOT = "True_vs_Estimated_Emissions_relative_differences.png"
    TRUE_AND_ESTIMATED_PAIRED_EMISSIONS_DISTRIBUTION_PLOT = (
        "True_and_Estimated_Paired_Emissions_Distribution.png"
    )
    EMISSIONS_SUMMARY_FILE = "emissions_summary.csv"
    EST_EMISSIONS_FILE = "estimated_emissions.csv"
    EST_REP_EMISSIONS_FILE = "estimated_repaired_emissions_to_remove.csv"
    TIMESERIES_FILE = "timeseries.csv"
    PARAMETER_FILE = "parameters.yaml"
