"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:   infrastructure_const 
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
        REP_EMIS_ERS = "repairable_ERS"  # Repairable Emissions: Emissions Rate Source
        REP_EMIS_EPR = "repairable_EPR"  # Repairable Emissions : Emission Production Rate
        REP_EMIS_RD = "repairable_RD"  # Repairable Emissions : Repair Delay
        REP_EMIS_RC = "repairable_RC"  # Repairable Emissions : Repair Cost
        REP_EMIS_ED = "repairable_ED"  # Repairable Emissions : Emissions Duration
        NON_REP_EMIS_ERS = "non_repairable_ERS"  # Non-Repairable Emissions: Emissions Rate Source
        NON_REP_EMIS_EPR = (
            "non_repairable_EPR"  # Non-Repairable Emissions: Emissions Production Rate
        )
        NON_REP_EMIS_ED = "non_repairable_ED"  # Non-Repairable Emissions: Emissions Duration
        SURVEY_FREQUENCY_PLACEHOLDER = "_surveyfreq"  # Survey Frequency - Method specific
        DEPLOYMENT_YEARS_PLACEHOLDER = "_deploy_year"  # Deployment Year - Method specific
        DEPLOYMENT_MONTHS_PLACEHOLDER = "_deploy_month"  # Deployment Month - Method specific
        SPATIAL_PLACEHOLDER = "_spatial"  # Spatial coverage - Method specific
        SURVEY_TIME_PLACEHOLDER = "_surveytime"  # Survey Time - Method specific
        SURVEY_COST_PLACEHOLDER = "_surveycost"  # Survey Cost - Method specific
        MIN_TIME_BT_SURVEYS_PLACEHOLDER = (
            "_min_time_bt_surveys"  # Minimum days between LDAR surveys - Method specific
        )

        PROPAGATING_PARAMS: list[str] = [
            REP_EMIS_ERS,
            REP_EMIS_EPR,
            REP_EMIS_RD,
            REP_EMIS_RC,
            REP_EMIS_ED,
            NON_REP_EMIS_ERS,
            NON_REP_EMIS_EPR,
            NON_REP_EMIS_ED,
        ]

        METH_SPEC_PROP_PARAMS: list[str] = [
            SPATIAL_PLACEHOLDER,
            SURVEY_FREQUENCY_PLACEHOLDER,
            SURVEY_COST_PLACEHOLDER,
            SURVEY_TIME_PLACEHOLDER,
        ]

        REQUIRED_HEADERS: list[str] = [ID, LAT, LON, TYPE]

        OPTIONAL_SHARED_HEADERS: list[str] = [EQG]

    class Equipment_Group_File_Constants:
        EQUIPMENT_GROUP = "equipment"  # Equipment Group
        REP_EMIS_ERS = "repairable_ERS"  # Repairable Emissions Rate Source
        REP_EMIS_EPR = "repairable_EPR"  # Repairable Emissions Production Rate
        REP_EMIS_RD = "repairable_RD"  # Repairable Emissions Repair Delay
        REP_EMIS_RC = "repairable_RC"  # Repairable Emissions Repair Cost
        REP_EMIS_ED = "repairable_ED"  # Repairable Emissions Emissions Duration
        NON_REP_EMIS_ERS = "non_repairable_ERS"  # Non-Repairable Emissions Rate Source
        NON_REP_EMIS_EPR = "non_repairable_EPR"  # Non-Repairable Emissions Production Rate
        NON_REP_EMIS_ED = "non_repairable_ED"  # Non-Repairable Emissions: Emissions Duration
        SURVEY_TIME_PLACEHOLDER = "_surveytime"  # Survey Time - Method specific
        SURVEY_COST_PLACEHOLDER = "_surveycost"  # Survey Cost - Method specific
        SPATIAL_PLACEHOLDER = "_spatial"  # Spatial coverage - Method specific

    class Sources_File_Constants:
        COMPONENT = "component"
        SOURCE = "source"
        EMIS_EPR = "EPR"
        EMIS_ERS = "ERS"  # Emission rate source
        EMIS_DUR = "ED"  # Emission Duration
        REPAIR_DELAY = "RD"  # Repair Delay
        REPAIR_COST = "RC"  # Repair Cost
        PERSISTENT = "persistent"  # Persistent (Y/N)
        REPAIRABLE = "repairable"  # Repairable (Y/N)
        ACTIVE_DUR = "active_dur"  # Active Duration
        INACTIVE_DUR = "inactive_dur"  # Inactive Duration
        SURVEY_TIME_PLACEHOLDER = "_surveytime"  # Survey Time - Method specific
        SURVEY_COST_PLACEHOLDER = "_surveycost"  # Survey Cost - Method specific
        SPATIAL_PLACEHOLDER = "_spatial"  # Spatial coverage - Method specific

    class Site_Type_File_Constants:
        TYPE = "site_type"  # Site Type
        EQG = "equipment"  # Equipment Group
        REP_EMIS_ERS = "repairable_ERS"  # Repairable Emissions: Emissions Rate Source
        REP_EMIS_EPR = "repairable_EPR"  # Repairable Emissions : Emission Production Rate
        REP_EMIS_RD = "repairable_RD"  # Repairable Emissions : Repair Delay
        REP_EMIS_RC = "repairable_RC"  # Repairable Emissions : Repair Cost
        REP_EMIS_ED = "repairable_ED"  # Repairable Emissions : Emissions Duration
        NON_REP_EMIS_ERS = "non_repairable_ERS"  # Non-Repairable Emissions: Emissions Rate Source
        NON_REP_EMIS_EPR = (
            "non_repairable_EPR"  # Non-Repairable Emissions: Emissions Production Rate
        )
        NON_REP_EMIS_ED = "non_repairable_ED"  # Non-Repairable Emissions: Emissions Duration
        SURVEY_FREQUENCY_PLACEHOLDER = "_surveyfreq"  # Survey Frequency - Method specific
        SPATIAL_PLACEHOLDER = "_spatial"  # Spatial coverage - Method specific
        SURVEY_TIME_PLACEHOLDER = "_surveytime"  # Survey Time - Method specific
        SURVEY_COST_PLACEHOLDER = "_surveycost"  # Survey Cost - Method specific
        MIN_TIME_BT_SURVEYS_PLACEHOLDER = (
            "_min_time_bt_surveys"  # Minimum days between LDAR surveys - Method specific
        )
        DEPLOYMENT_YEARS_PLACEHOLDER = "_deploy_year"  # Deployment Year - Method specific
        DEPLOYMENT_MONTHS_PLACEHOLDER = "_deploy_month"  # Deployment Month - Method specific

        PROPAGATING_PARAMS: list[str] = [
            REP_EMIS_ERS,
            REP_EMIS_EPR,
            REP_EMIS_RD,
            REP_EMIS_RC,
            REP_EMIS_ED,
            NON_REP_EMIS_ERS,
            NON_REP_EMIS_EPR,
            NON_REP_EMIS_ED,
        ]

        METH_SPEC_PROP_PARAMS: list[str] = [
            SPATIAL_PLACEHOLDER,
            SURVEY_FREQUENCY_PLACEHOLDER,
            SURVEY_COST_PLACEHOLDER,
            SURVEY_TIME_PLACEHOLDER,
            DEPLOYMENT_MONTHS_PLACEHOLDER,
            DEPLOYMENT_YEARS_PLACEHOLDER,
        ]


class Virtual_World_To_Prop_Params_Mapping:
    PROPAGATING_PARAMS: dict[str, str] = {
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ERS: "emissions.ERS",
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_EPR: "emissions.LPR",
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RD: "repairs.delay",
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RC: "repairs.cost",
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ED: "emissions.NRd",
        Infrastructure_Constants.Sites_File_Constants.NON_REP_EMIS_ERS: "emissions.NR_ERS",
        Infrastructure_Constants.Sites_File_Constants.NON_REP_EMIS_EPR: "emissions.NR_EPR",
        Infrastructure_Constants.Sites_File_Constants.NON_REP_EMIS_ED: "emissions.duration",
    }

    METH_SPEC_PROP_PARAMS: dict[str, str] = {
        Infrastructure_Constants.Sites_File_Constants.SPATIAL_PLACEHOLDER: "coverage.spatial",  # noqa
        Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER: "RS",
        Infrastructure_Constants.Sites_File_Constants.SURVEY_COST_PLACEHOLDER: "cost.per_site",
        Infrastructure_Constants.Sites_File_Constants.SURVEY_TIME_PLACEHOLDER: "time",
        Infrastructure_Constants.Sites_File_Constants.MIN_TIME_BT_SURVEYS_PLACEHOLDER: "scheduling.min_time_bt_surveys",  # noqa
        Infrastructure_Constants.Sites_File_Constants.MIN_TIME_BT_SURVEYS_PLACEHOLDER: "scheduling.min_time_bt_surveys",  # noqa
        Infrastructure_Constants.Site_Type_File_Constants.DEPLOYMENT_MONTHS_PLACEHOLDER: "scheduling.deployment_months",  # noqa
        Infrastructure_Constants.Site_Type_File_Constants.DEPLOYMENT_YEARS_PLACEHOLDER: "scheduling.deployment_years",  # noqa
    }
