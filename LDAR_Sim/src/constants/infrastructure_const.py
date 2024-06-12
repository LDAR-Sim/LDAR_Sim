"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:   infrastructure_const.py
Purpose: The file contains constants used for the infrastructure module

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

from constants import param_default_const


class Infrastructure_Constants:
    class Virtual_World_Constants:
        SOURCES = "sources"
        EQG = "equipment"
        SITES = "sites"
        SITE_TYPE = "site_type"

    class Sites_File_Constants:
        LAT = "lat"  # Latitude
        LON = "lon"  # Longitude
        ID = "site_ID"  # Site ID
        TYPE = "site_type"  # Site Type
        EQG = "equipment"  # Equipment Group
        REP_EMIS_ERS = (
            "repairable_emissions_rate_source"  # Repairable Emissions: Emissions Rate Source
        )
        # Repairable Emissions : Emission Production Rate
        REP_EMIS_EPR = "repairable_emissions_production_rate"
        REP_EMIS_RD = "repairable_repair_delay"  # Repairable Emissions : Repair Delay
        REP_EMIS_RC = "repairable_repair_cost"  # Repairable Emissions : Repair Cost
        REP_EMIS_ED = "repairable_duration"  # Repairable Emissions : Emissions Duration
        REP_EMIS_MULTI = (
            "repairable_multiple_emissions_per_source"  # Repairable Emissions : Multiple Emissions
        )
        # Non-Repairable Emissions: Emissions Rate Source
        NON_REP_EMIS_ERS = "non_repairable_emissions_rate_source"
        # Non-Repairable Emissions: Emissions Production Rate
        NON_REP_EMIS_EPR = "non_repairable_emissions_production_rate"
        NON_REP_EMIS_ED = "non_repairable_duration"  # Non-Repairable Emissions: Emissions Duration
        # Non-Repairable Emissions: Multiple Emissions
        NON_REP_EMIS_MULTI = "non_repairable_multiple_emissions_per_source"
        SURVEY_FREQUENCY_PLACEHOLDER = "_surveys_per_year"  # Survey Frequency - Method specific
        DEPLOYMENT_YEARS_PLACEHOLDER = "_deploy_year"  # Deployment Year - Method specific
        DEPLOYMENT_MONTHS_PLACEHOLDER = "_deploy_month"  # Deployment Month - Method specific
        SPATIAL_PLACEHOLDER = "_spatial"  # Spatial coverage - Method specific
        SURVEY_TIME_PLACEHOLDER = "_survey_time"  # Survey Time - Method specific
        SURVEY_COST_PLACEHOLDER = "_survey_cost"  # Survey Cost - Method specific

        SITE_DEPLOYMENT_PLACEHOLDER = "_site_deployment"  # Site deployment - Method specific

        PROPAGATING_PARAMS: list[str] = [
            REP_EMIS_ERS,
            REP_EMIS_EPR,
            REP_EMIS_RD,
            REP_EMIS_RC,
            REP_EMIS_ED,
            REP_EMIS_MULTI,
            NON_REP_EMIS_ERS,
            NON_REP_EMIS_EPR,
            NON_REP_EMIS_ED,
            NON_REP_EMIS_MULTI,
        ]

        METH_SPEC_PROP_PARAMS: list[str] = [
            SPATIAL_PLACEHOLDER,
            SURVEY_FREQUENCY_PLACEHOLDER,
            SURVEY_COST_PLACEHOLDER,
            SURVEY_TIME_PLACEHOLDER,
            SITE_DEPLOYMENT_PLACEHOLDER,
            DEPLOYMENT_MONTHS_PLACEHOLDER,
            DEPLOYMENT_YEARS_PLACEHOLDER,
        ]

        REQUIRED_HEADERS: list[str] = [ID, LAT, LON, TYPE]

        OPTIONAL_SHARED_HEADERS: list[str] = [EQG]

    class Equipment_Group_File_Constants:
        EQUIPMENT_GROUP = "equipment"  # Equipment Group
        REP_EMIS_ERS = "repairable_emissions_rate_source"  # Repairable Emissions Rate Source
        REP_EMIS_EPR = (
            "repairable_emissions_production_rate"  # Repairable Emissions Production Rate
        )
        REP_EMIS_RD = "repairable_repair_delay"  # Repairable Emissions Repair Delay
        REP_EMIS_RC = "repairable_repair_cost"  # Repairable Emissions Repair Cost
        REP_EMIS_ED = "repairable_duration"  # Repairable Emissions Emissions Duration
        REP_EMIS_MULTI = (
            "repairable_multiple_emissions_per_source"  # Repairable Emissions Multiple Emissions
        )
        NON_REP_EMIS_ERS = (
            "non_repairable_emissions_rate_source"  # Non-Repairable Emissions Rate Source
        )
        NON_REP_EMIS_EPR = (
            "non_repairable_emissions_production_rate"  # Non-Repairable Emissions Production Rate
        )
        NON_REP_EMIS_ED = "non_repairable_duration"  # Non-Repairable Emissions: Emissions Duration
        # Non-Repairable Emissions Multiple Emissions
        NON_REP_EMIS_MULTI = "non_repairable_multiple_emissions_per_source"
        SURVEY_TIME_PLACEHOLDER = "_survey_time"  # Survey Time - Method specific
        SURVEY_COST_PLACEHOLDER = "_survey_cost"  # Survey Cost - Method specific
        SPATIAL_PLACEHOLDER = "_spatial"  # Spatial coverage - Method specific

    class Sources_File_Constants:
        COMPONENT = "component"
        SOURCE = "source"
        EMIS_EPR = "emissions_production_rate"
        EMIS_ERS = "emissions_rate_source"  # Emission rate source
        EMIS_DUR = "duration"  # Emission Duration
        REPAIR_DELAY = "repair_delay"  # Repair Delay
        REPAIR_COST = "repair_cost"  # Repair Cost
        PERSISTENT = "persistent"  # Persistent (Y/N)
        REPAIRABLE = "repairable"  # Repairable (Y/N)
        ACTIVE_DUR = "active_duration"  # Active Duration
        INACTIVE_DUR = "inactive_duration"  # Inactive Duration
        SURVEY_TIME_PLACEHOLDER = "_survey_time"  # Survey Time - Method specific
        SURVEY_COST_PLACEHOLDER = "_survey_cost"  # Survey Cost - Method specific
        SPATIAL_PLACEHOLDER = "_spatial"  # Spatial coverage - Method specific
        MULTI_EMISSIONS = "multiple_emissions_per_source"  # Multiple Emissions (Y/N)

    class Site_Type_File_Constants:
        TYPE = "site_type"  # Site Type
        EQG = "equipment"  # Equipment Group
        REP_EMIS_ERS = (
            "repairable_emissions_rate_source"  # Repairable Emissions: Emissions Rate Source
        )
        # Repairable Emissions : Emission Production Rate
        REP_EMIS_EPR = "repairable_emissions_production_rate"
        REP_EMIS_RD = "repairable_repairs_delay"  # Repairable Emissions : Repair Delay
        REP_EMIS_RC = "repairable_repairs_cost"  # Repairable Emissions : Repair Cost
        REP_EMIS_ED = "repairable_duration"  # Repairable Emissions : Emissions Duration
        REP_EMIS_MULTI = (
            "repairable_multiple_emissions_per_source"  # Repairable Emissions : Multiple Emissions
        )
        # Non-Repairable Emissions: Emissions Rate Source
        NON_REP_EMIS_ERS = "non_repairable_emissions_rate_source"
        # Non-Repairable Emissions: Emissions Production Rate
        NON_REP_EMIS_EPR = "non_repairable_emissions_production_rate"
        NON_REP_EMIS_ED = "non_repairable_duration"  # Non-Repairable Emissions: Emissions Duration
        # Non-Repairable Emissions: Multiple Emissions
        NON_REP_EMIS_MULTI = "non_repairable_multiple_emissions_per_source"
        SURVEY_FREQUENCY_PLACEHOLDER = "_surveys_per_year"  # Survey Frequency - Method specific
        SPATIAL_PLACEHOLDER = "_spatial"  # Spatial coverage - Method specific
        SURVEY_TIME_PLACEHOLDER = "_survey_time"  # Survey Time - Method specific
        SURVEY_COST_PLACEHOLDER = "_survey_cost"  # Survey Cost - Method specific
        DEPLOYMENT_YEARS_PLACEHOLDER = "_deploy_year"  # Deployment Year - Method specific
        DEPLOYMENT_MONTHS_PLACEHOLDER = "_deploy_month"  # Deployment Month - Method specific

        SITE_DEPLOYMENT_PLACEHOLDER = "_site_deployment"  # Site deployment - Method specific

        PROPAGATING_PARAMS: list[str] = [
            REP_EMIS_ERS,
            REP_EMIS_EPR,
            REP_EMIS_RD,
            REP_EMIS_RC,
            REP_EMIS_ED,
            REP_EMIS_MULTI,
            NON_REP_EMIS_ERS,
            NON_REP_EMIS_EPR,
            NON_REP_EMIS_ED,
            NON_REP_EMIS_MULTI,
        ]

        METH_SPEC_PROP_PARAMS: list[str] = [
            SPATIAL_PLACEHOLDER,
            SURVEY_FREQUENCY_PLACEHOLDER,
            SURVEY_COST_PLACEHOLDER,
            SURVEY_TIME_PLACEHOLDER,
            DEPLOYMENT_MONTHS_PLACEHOLDER,
            DEPLOYMENT_YEARS_PLACEHOLDER,
            SITE_DEPLOYMENT_PLACEHOLDER,
        ]


class Deployment_TF_Sites_Constants:
    SITE_ID = Infrastructure_Constants.Sites_File_Constants.ID
    SITE_TYPE = Infrastructure_Constants.Sites_File_Constants.TYPE
    REQUIRED_SURVEY: str = (
        "{method}" + Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER
    )
    SITE_DEPLOYMENT: str = (
        "{method}" + Infrastructure_Constants.Sites_File_Constants.SITE_DEPLOYMENT_PLACEHOLDER
    )
    SITE_MEASURED: str = "{method}_measured"


class Virtual_World_To_Prop_Params_Mapping:
    PROPAGATING_PARAMS: dict[str, str] = {
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ERS: ".".join(
            [
                param_default_const.Virtual_World_Params.EMIS,
                param_default_const.Virtual_World_Params.REPAIRABLE,
                param_default_const.Virtual_World_Params.ERS,
            ]
        ),
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_EPR: ".".join(
            [
                param_default_const.Virtual_World_Params.EMIS,
                param_default_const.Virtual_World_Params.REPAIRABLE,
                param_default_const.Virtual_World_Params.PR,
            ]
        ),
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RD: ".".join(
            [
                param_default_const.Virtual_World_Params.REPAIR,
                param_default_const.Virtual_World_Params.REPAIR_DELAY,
            ]
        ),
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RC: ".".join(
            [
                param_default_const.Virtual_World_Params.REPAIR,
                param_default_const.Virtual_World_Params.REPAIR_COST,
            ]
        ),
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ED: ".".join(
            [
                param_default_const.Virtual_World_Params.EMIS,
                param_default_const.Virtual_World_Params.REPAIRABLE,
                param_default_const.Virtual_World_Params.DURATION,
            ]
        ),
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_MULTI: ".".join(
            [
                param_default_const.Virtual_World_Params.EMIS,
                param_default_const.Virtual_World_Params.REPAIRABLE,
                param_default_const.Virtual_World_Params.MULTI_EMIS,
            ]
        ),
        Infrastructure_Constants.Sites_File_Constants.NON_REP_EMIS_ERS: ".".join(
            [
                param_default_const.Virtual_World_Params.EMIS,
                param_default_const.Virtual_World_Params.NON_REPAIRABLE,
                param_default_const.Virtual_World_Params.ERS,
            ]
        ),
        Infrastructure_Constants.Sites_File_Constants.NON_REP_EMIS_EPR: ".".join(
            [
                param_default_const.Virtual_World_Params.EMIS,
                param_default_const.Virtual_World_Params.NON_REPAIRABLE,
                param_default_const.Virtual_World_Params.PR,
            ]
        ),
        Infrastructure_Constants.Sites_File_Constants.NON_REP_EMIS_ED: ".".join(
            [
                param_default_const.Virtual_World_Params.EMIS,
                param_default_const.Virtual_World_Params.NON_REPAIRABLE,
                param_default_const.Virtual_World_Params.DURATION,
            ]
        ),
        Infrastructure_Constants.Sites_File_Constants.NON_REP_EMIS_MULTI: ".".join(
            [
                param_default_const.Virtual_World_Params.EMIS,
                param_default_const.Virtual_World_Params.NON_REPAIRABLE,
                param_default_const.Virtual_World_Params.MULTI_EMIS,
            ]
        ),
    }

    METH_SPEC_PROP_PARAMS: dict[str, str] = {
        Infrastructure_Constants.Sites_File_Constants.SPATIAL_PLACEHOLDER: ".".join(
            [param_default_const.Method_Params.COVERAGE, param_default_const.Method_Params.SPATIAL]
        ),
        (
            Infrastructure_Constants.Sites_File_Constants
        ).SURVEY_FREQUENCY_PLACEHOLDER: param_default_const.Method_Params.RS,
        (Infrastructure_Constants.Sites_File_Constants).SURVEY_COST_PLACEHOLDER: ".".join(
            [param_default_const.Method_Params.COST, param_default_const.Method_Params.PER_SITE]
        ),
        (
            Infrastructure_Constants.Sites_File_Constants
        ).SURVEY_TIME_PLACEHOLDER: param_default_const.Method_Params.TIME,
        (Infrastructure_Constants.Site_Type_File_Constants).DEPLOYMENT_MONTHS_PLACEHOLDER: ".".join(
            [
                param_default_const.Method_Params.SCHEDULING,
                param_default_const.Method_Params.DEPLOYMENT_MONTHS,
            ]
        ),
        (Infrastructure_Constants.Site_Type_File_Constants).DEPLOYMENT_YEARS_PLACEHOLDER: ".".join(
            [
                param_default_const.Method_Params.SCHEDULING,
                param_default_const.Method_Params.DEPLOYMENT_YEARS,
            ]
        ),
    }
