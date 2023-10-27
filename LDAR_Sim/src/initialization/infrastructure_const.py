"""
Contains constants for infrastructure
"""


class Infrastructure_Constants:
    class Sites_File_Constants:
        LAT = "lat"  # Latitude
        LON = "lon"  # Longitude
        ID = "site_ID"  # Site ID
        TYPE = "site_type"  # Site Type
        EQG = "equipment_group"  # Equipment Group
        REP_EMIS_ERS = "repairable_ERS"  # Repairable Emissions: Emissions Rate Source
        REP_EMIS_EPR = "repairable_EPR"  # Repairable Emissions : Emission Production Rate
        REP_EMIS_RD = "repairable_RD"  # Repairable Emissions : Repair Delay
        REP_EMIS_RC = "repairable_RC"  # Repairable Emissions : Repair Cost
        REP_EMIS_ED = "repairable_ED"  # Repairable Emissions : Emissions Duration
        NON_REP_EMIS_ERS = "non_repairable_ERS"  # Non-Repairable Emissions: Emissions Rate Source
        SURVEY_FREQUENCY_PLACEHOLDER = "_surveyfreq"  # Survey Frequency - Method specific
        SPATIAL_PLACEHOLDER = "_spatial"  # Spatial coverage - Method specific
        SURVEY_TIME_PLACEHOLDER = "_surveytime"  # Survey Time - Method specific
        SURVEY_COST_PLACEHOLDER = "_surveycost"  # Survey Cost - Method specific

    class Equipment_Group_File_Constants:
        EQUIPMENT_GROUP = "equip_group"  # Equipment Group
        REP_EMIS_ERS_PLACEHOLDER = "_repairable_ERS"  # Repairable Emissions Rate Source
        REP_EMIS_EPR_PLACEHOLDER = "_repairable_EPR"  # Repairable Emissions Production Rate
        REP_EMIS_RD_PLACEHOLDER = "_repairable_RD"  # Repairable Emissions Repair Delay
        REP_EMIS_RC_PLACEHOLDER = "_repairable_RC"  # Repairable Emissions Repair Cost
        REP_EMIS_ED_PLACEHOLDER = "_repairable_ED"  # Repairable Emissions Emissions Duration
        NON_REP_EMIS_ERS_PLACEHOLDER = "_non_repairable_ERS"  # Non-Repairable Emissions Rate Source
        SURVEY_TIME_PLACEHOLDER = "_surveytime"  # Survey Time - Method specific
        SURVEY_COST_PLACEHOLDER = "_surveycost"  # Survey Cost - Method specific
        SPATIAL_PLACEHOLDER = "_spatial"  # Spatial coverage - Method specific

    class Sources_File_Constants:
        EQUIPMENT = "equipment"
        SOURCE = "source"
        EMIS_EPR = "production rate"
        EMIS_ERS = "ERS"  # Emission rate source
        EMISS_DUR = "emiss_dur"  # Emission Duration
        REPAIR_DELAY = "rep_delay"  # Repair Delay
        REPAIR_COST = "rep_cost"  # Repair Cost
        PERSISTENT = "persistent"  # Persistent (Y/N)
        REPAIRABLE = "repairable"  # Repairable (Y/N)
        ACTIVE_DUR = "active_dur"  # Active Duration
        INACTIVE_DUR = "inactive_dur"  # Inactive Duration
        SURVEY_TIME_PLACEHOLDER = "_surveytime"  # Survey Time - Method specific
        SURVEY_COST_PLACEHOLDER = "_surveycost"  # Survey Cost - Method specific
        SPATIAL_PLACEHOLDER = "_spatial"  # Spatial coverage - Method specific

    class Site_Type_File_Constants:
        TYPE = "site_type"  # Site Type
        EQG = "equipment_group"  # Equipment Group
        REP_EMIS_ERS = "repairable_ERS"  # Repairable Emissions: Emissions Rate Source
        REP_EMIS_EPR = "repairable_EPR"  # Repairable Emissions : Emission Production Rate
        REP_EMIS_RD = "repairable_RD"  # Repairable Emissions : Repair Delay
        REP_EMIS_RC = "repairable_RC"  # Repairable Emissions : Repair Cost
        REP_EMIS_ED = "repairable_ED"  # Repairable Emissions : Emissions Duration
        NON_REP_EMIS_ERS = "non_repairable_ERS"  # Non-Repairable Emissions: Emissions Rate Source
        SURVEY_FREQUENCY_PLACEHOLDER = "_surveyfreq"  # Survey Frequency - Method specific
        SPATIAL_PLACEHOLDER = "_spatial"  # Spatial coverage - Method specific
        SURVEY_TIME_PLACEHOLDER = "_surveytime"  # Survey Time - Method specific
        SURVEY_COST_PLACEHOLDER = "_surveycost"  # Survey Cost - Method specific
