"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        program_output.py
Purpose: This is where the functions to define how duration estimation reports
are stored. Users would want to add to this file and the mapper in the 
program_output_manager.py file if they want to add new reports.

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

import pandas as pd
from datetime import date

from file_processing.output_processing import program_output_helpers
from scheduling.schedule_dataclasses import (
    SiteSurveyReport,
)
from constants.output_file_constants import (
    EMIS_DATA_COL_ACCESSORS as eca,
    EMIS_ESTIMATION_OUTPUT_COLUMNS,
    EMIS_COMP_ESTIMATION_OUTPUT_COLUMNS,
    EST_FUG_OUTPUT_COLUMNS,
)
from constants.file_name_constants import Output_Files


def gen_estimated_fugitive_emissions_to_remove(
    site_survey_reports_summary: pd.DataFrame,
    fugitive_emissions_rates_and_repair_dates: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate a report of yearly estimated fugitive emissions to remove to avoid double counting
    """
    if fugitive_emissions_rates_and_repair_dates.empty:
        return pd.DataFrame()
    # Switch the data types of repair date column to datetime so date computations can be done
    fugitive_emissions_rates_and_repair_dates[eca.DATE_REP_EXP] = (
        fugitive_emissions_rates_and_repair_dates.loc[:, eca.DATE_REP_EXP].astype("datetime64[ns]")
    )

    # Drop rows with missing repair dates
    fugitive_emissions_rates_and_repair_dates.dropna(inplace=True)

    # Populate a new column in the fugitive emissions rates and repair dates dataframe
    # with the closest future survey date. This wil be used to compute the estimated
    # fugitive emissions to remove to avoid double counting
    # Create a dictionary to store the unique survey completion dates for each site
    site_survey_dates = (
        site_survey_reports_summary.groupby(eca.SITE_ID)[eca.SURVEY_COMPLETION_DATE]
        .unique()
        .to_dict()
    )

    # Use the dictionary to map the closest future survey date for each row
    fugitive_emissions_rates_and_repair_dates[eca.NEXT_SURVEY_DATE] = (
        fugitive_emissions_rates_and_repair_dates.apply(
            lambda x: program_output_helpers.closest_future_date(
                x[eca.DATE_REP_EXP], site_survey_dates[x[eca.SITE_ID]]
            ),
            axis=1,
        )
    )
    fugitive_emissions_rates_and_repair_dates.loc[
        :, "account_for_fugitives"
    ] = fugitive_emissions_rates_and_repair_dates.loc[:, eca.NEXT_SURVEY_DATE].apply(
        lambda x: program_output_helpers.find_df_row_value_w_match(
            x,
            eca.SURVEY_COMPLETION_DATE,
            eca.PREV_CONDITION,
            site_survey_reports_summary,
        )
    )
    fugitive_emissions_rates_and_repair_dates.drop(
        fugitive_emissions_rates_and_repair_dates.index[
            ~fugitive_emissions_rates_and_repair_dates["account_for_fugitives"]
        ],
        inplace=True,
    )

    # Assign the Start and End date based on the repaired/expiry date and the next survey date
    # to be able to re-use the calculate_volume_emitted function
    # to calculate the emissions to remove
    fugitive_emissions_rates_and_repair_dates = fugitive_emissions_rates_and_repair_dates.assign(
        **{eca.START_DATE: lambda x: x[eca.DATE_REP_EXP]},
        **{eca.END_DATE: lambda x: x[eca.NEXT_SURVEY_DATE]},
    )
    fugitive_emissions_rates_and_repair_dates[eca.EST_VOL_EMIT] = (
        fugitive_emissions_rates_and_repair_dates.apply(
            program_output_helpers.calculate_volume_emitted, axis=1
        )
    )

    return fugitive_emissions_rates_and_repair_dates[EST_FUG_OUTPUT_COLUMNS]


def gen_estimated_emissions_report(
    pm,
    site_survey_reports_summary: pd.DataFrame,
    fugutive_emissions_rates_and_repair_dates: pd.DataFrame,
    start_date: date,
    end_date: date,
) -> None:
    """Generate a report of yearly estimated emissions based on site survey reports
    Args:
        site_survey_reports (pd.DataFrame): The site survey reports
        output_dir (str): The output directory
    """
    # return if no survey reports
    if site_survey_reports_summary.empty:
        return

    # Get unique site ids
    site_ids: list = site_survey_reports_summary[eca.SITE_ID].unique()

    # For all sites, add a survey report for the start and end date of the simulation
    site_survey_data: list = []

    for site_id in site_ids:
        start_report = SiteSurveyReport(
            site_id=site_id, survey_start_date=start_date, survey_completion_date=start_date
        ).to_report_summary()
        site_survey_data.append(start_report)
        end_report = SiteSurveyReport(
            site_id=site_id, survey_start_date=end_date, survey_completion_date=end_date
        ).to_report_summary()
        site_survey_data.append(end_report)

    new_site_survey_data: pd.DataFrame = pd.DataFrame(site_survey_data)
    site_survey_reports_summary = pd.concat([site_survey_reports_summary, new_site_survey_data])

    site_survey_reports_summary[eca.SURVEY_COMPLETION_DATE] = site_survey_reports_summary[
        eca.SURVEY_COMPLETION_DATE
    ].astype("datetime64[ns]")

    sorted_by_site_summary = site_survey_reports_summary.sort_values(
        by=[eca.SITE_ID, eca.SURVEY_COMPLETION_DATE]
    ).reset_index(drop=True)

    grouped_by_site_summary = sorted_by_site_summary.groupby(eca.SITE_ID)

    # Calculate the days since last survey and days till next survey based on the survey completion date
    sorted_by_site_summary["days_since_last_survey"] = (
        grouped_by_site_summary[eca.SURVEY_COMPLETION_DATE].diff().dt.days
    )
    sorted_by_site_summary["days_since_last_survey"] = (
        grouped_by_site_summary[eca.SURVEY_COMPLETION_DATE].diff().dt.days
    )
    sorted_by_site_summary["days_until_next_survey"] = abs(
        grouped_by_site_summary[eca.SURVEY_COMPLETION_DATE].diff(-1).dt.days
    )
    # Calculate if the previous or the next condition should be used for the emission rate
    sorted_by_site_summary[eca.PREV_CONDITION] = grouped_by_site_summary[eca.M_RATE].diff() <= 0
    sorted_by_site_summary[eca.NEXT_CONDITION] = grouped_by_site_summary[eca.M_RATE].diff(-1) < 0

    # Set the estimated start/end date based on the emission rate condition
    sorted_by_site_summary[eca.START_DATE] = (
        sorted_by_site_summary.groupby(eca.SITE_ID)
        .apply(program_output_helpers.calculate_start_date)
        .reset_index(drop=True)
    )
    sorted_by_site_summary[eca.END_DATE] = (
        sorted_by_site_summary.groupby(eca.SITE_ID)
        .apply(program_output_helpers.calculate_end_date)
        .reset_index(drop=True)
    )
    # Generate a report of estimated fugitive emissions to remove
    fugitive_emissions_to_remove: pd.DataFrame = gen_estimated_fugitive_emissions_to_remove(
        site_survey_reports_summary=sorted_by_site_summary,
        fugitive_emissions_rates_and_repair_dates=fugutive_emissions_rates_and_repair_dates,
    )
    # Calculate the estimated volume emitted based on the start/end date and measured rate columns
    sorted_by_site_summary[eca.EST_VOL_EMIT] = sorted_by_site_summary.apply(
        program_output_helpers.calculate_volume_emitted, axis=1
    ).reset_index(drop=True)

    # Select only the predefined columns
    selected_sorted_by_site_summary = sorted_by_site_summary[EMIS_ESTIMATION_OUTPUT_COLUMNS]

    rep_filename: str = pm.generate_file_names(Output_Files.EST_REP_EMISSIONS_FILE)
    filename: str = pm.generate_file_names(Output_Files.EST_EMISSIONS_FILE)

    selected_sorted_by_site_summary.to_csv(pm._output_dir / filename, index=False)
    fugitive_emissions_to_remove.to_csv(pm._output_dir / rep_filename, index=False)


def gen_estimated_comp_emissions_report(
    pm,
    site_survey_reports_summary: pd.DataFrame,
    fugutive_emissions_rates_and_repair_dates: pd.DataFrame,
    start_date: date,
    end_date: date,
) -> None:
    """Generate a report of yearly estimated emissions based on only component level surveys
    Args:
        site_survey_reports (pd.DataFrame): The site survey reports
        output_dir (str): The output directory
    """
    if site_survey_reports_summary.empty:
        return

    # Unpack the site survey reports to return equipment and component level survey reports
    unpack_equip = program_output_helpers.expand_column(site_survey_reports_summary, eca.EQG)
    unpack_comp = program_output_helpers.expand_column(unpack_equip, eca.COMP)

    # Filter out only the component level survey reports
    unpack_comp = unpack_comp[unpack_comp[eca.SURVEY_LEVEL] == "component_level"]
    # Get unique combinations of site_ID, equipment and component
    unique_combinations = unpack_comp[[eca.SITE_ID, eca.EQG, eca.COMP]].drop_duplicates()
    unique_site_survey_dates = unpack_comp[
        [eca.SITE_ID, eca.SURVEY_COMPLETION_DATE]
    ].drop_duplicates()

    # Convert to a list of tuples
    unique_combinations_list = list(unique_combinations.itertuples(index=False, name=None))

    unique_site_survey_dates = list(unique_site_survey_dates.itertuples(index=False, name=None))

    # Create a set of tuples for all existing combinations in the DataFrame
    existing_combinations = set(
        zip(
            unpack_comp[eca.SITE_ID],
            unpack_comp[eca.EQG],
            unpack_comp[eca.COMP],
            unpack_comp[eca.SURVEY_COMPLETION_DATE],
        )
    )

    # For each site/equipment/component combination, add in the missing reports for when there were 0
    # detections for a given component at a given date
    for site_id, eqg, comp in unique_combinations_list:
        # Get the unique dates for the current site_id from unique_site_survey_dates
        site_dates = set(u_date for site, u_date in unique_site_survey_dates if site == site_id)

        # Check if a date from site_dates exists for the current combination
        for s_date in site_dates:
            if (site_id, eqg, comp, s_date) not in existing_combinations:
                # If the date does not exist, add a new row with the current combination and date
                unpack_comp.loc[len(unpack_comp)] = {
                    eca.SITE_ID: site_id,
                    eca.EQG: eqg,
                    eca.COMP: comp,
                    eca.SURVEY_COMPLETION_DATE: s_date,
                    eca.M_RATE: 0,
                }
    # Adding start and end date for each unique component
    new_data: list = []
    for site_id, eqg, comp in unique_combinations_list:

        new_row_1: dict = {
            eca.SITE_ID: site_id,
            eca.EQG: eqg,
            eca.COMP: comp,
            eca.SURVEY_START_DATE: start_date,
            eca.SURVEY_COMPLETION_DATE: start_date,
            eca.M_RATE: 0,
        }

        new_row_2: dict = {
            eca.SITE_ID: site_id,
            eca.EQG: eqg,
            eca.COMP: comp,
            eca.SURVEY_START_DATE: end_date,
            eca.SURVEY_COMPLETION_DATE: end_date,
            eca.M_RATE: 0,
        }
        new_data.append(new_row_1)
        new_data.append(new_row_2)

    new_data_df: pd.DataFrame = pd.DataFrame(new_data)
    unpack_comp = pd.concat([unpack_comp, new_data_df], ignore_index=True)

    unpack_comp[eca.SURVEY_COMPLETION_DATE] = unpack_comp[eca.SURVEY_COMPLETION_DATE].astype(
        "datetime64[ns]"
    )
    # Sort by the composite key - site_id, equipment, component and survey completion date
    sorted_by_site_summary = unpack_comp.sort_values(
        by=[eca.SITE_ID, eca.EQG, eca.COMP, eca.SURVEY_COMPLETION_DATE]
    ).reset_index(drop=True)

    # For each unique site/equipment/component combination, calculate the days since last survey
    grouped_by_site_summary = sorted_by_site_summary.groupby([eca.SITE_ID, eca.EQG, eca.COMP])

    sorted_by_site_summary["days_since_last_survey"] = (
        grouped_by_site_summary[eca.SURVEY_COMPLETION_DATE].diff().dt.days
    )
    sorted_by_site_summary["days_since_last_survey"] = (
        grouped_by_site_summary[eca.SURVEY_COMPLETION_DATE].diff().dt.days
    )
    sorted_by_site_summary["days_until_next_survey"] = abs(
        grouped_by_site_summary[eca.SURVEY_COMPLETION_DATE].diff(-1).dt.days
    )
    # Determine if the previous or next condition should be used for the emission rate
    sorted_by_site_summary[eca.PREV_CONDITION] = grouped_by_site_summary[eca.M_RATE].diff() <= 0
    sorted_by_site_summary[eca.NEXT_CONDITION] = grouped_by_site_summary[eca.M_RATE].diff(-1) < 0
    # Set the estimated start/end date based on the emission rate condition
    sorted_by_site_summary[eca.START_DATE] = grouped_by_site_summary.apply(
        program_output_helpers.calculate_start_date
    ).reset_index(drop=True)
    sorted_by_site_summary[eca.END_DATE] = grouped_by_site_summary.apply(
        program_output_helpers.calculate_end_date
    ).reset_index(drop=True)

    fugitive_emissions_to_remove: pd.DataFrame = gen_estimated_fugitive_emissions_to_remove(
        site_survey_reports_summary=sorted_by_site_summary,
        fugitive_emissions_rates_and_repair_dates=fugutive_emissions_rates_and_repair_dates,
    )

    sorted_by_site_summary[eca.EST_VOL_EMIT] = sorted_by_site_summary.apply(
        program_output_helpers.calculate_volume_emitted, axis=1
    ).reset_index(drop=True)

    # Filter out only the predefined columns
    select_sorted_by_site_summary = sorted_by_site_summary[EMIS_COMP_ESTIMATION_OUTPUT_COLUMNS]
    # Save files
    rep_filename: str = pm.generate_file_names(Output_Files.EST_REP_EMISSIONS_FILE)
    filename: str = pm.generate_file_names(Output_Files.EST_EMISSIONS_FILE)

    select_sorted_by_site_summary.to_csv(pm._output_dir / filename, index=False)
    fugitive_emissions_to_remove.to_csv(pm._output_dir / rep_filename, index=False)
