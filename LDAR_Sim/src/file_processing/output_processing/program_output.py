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
    EST_FUG_OUTPUT_COLUMNS,
)


def gen_estimated_repairable_emissions_to_remove(
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

    # Drop rows with missing repair dates and missing measured rates
    fugitive_emissions_rates_and_repair_dates.dropna(inplace=True)

    if fugitive_emissions_rates_and_repair_dates.empty:
        return pd.DataFrame()

    # Populate a new column in the fugitive emissions rates and repair dates dataframe
    # with the closest future survey date. This wil be used to compute the estimated
    # fugitive emissions to remove to avoid double counting
    # Create a dictionary to store the unique survey completion dates for each site
    site_survey_dates = (
        site_survey_reports_summary.groupby(eca.SITE_ID)
        .apply(lambda df: list(zip(df[eca.SURVEY_COMPLETION_DATE], df[eca.START_DATE])))
        .to_dict()
    )
    # Use the dictionary to map the closest future survey date for each row
    fugitive_emissions_rates_and_repair_dates[eca.NEXT_SURVEY_DATE] = (
        fugitive_emissions_rates_and_repair_dates.apply(
            lambda x: program_output_helpers.find_closest_future_date(
                x[eca.DATE_REP_EXP], site_survey_dates[x[eca.SITE_ID]]
            ),
            axis=1,
        )
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
    site_survey_reports_summary: pd.DataFrame,
    fugutive_emissions_rates_and_repair_dates: pd.DataFrame,
    start_date: date,
    end_date: date,
    site_ids: list[str],
    duration_factor: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generate a report of yearly estimated emissions based on site survey reports
    Args:
        site_survey_reports (pd.DataFrame): The site survey reports
        output_dir (str): The output directory
    """
    # return if no survey reports
    if site_survey_reports_summary.empty:
        return

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

    sorted_by_site_summary = determine_start_and_end_dates(
        sorted_by_site_summary, grouped_by_site_summary, duration_factor
    )

    # Generate a report of estimated fugitive emissions to remove
    fugitive_emissions_to_remove: pd.DataFrame = gen_estimated_repairable_emissions_to_remove(
        site_survey_reports_summary=sorted_by_site_summary,
        fugitive_emissions_rates_and_repair_dates=fugutive_emissions_rates_and_repair_dates,
    )
    # Calculate the estimated volume emitted based on the start/end date and measured rate columns
    sorted_by_site_summary[eca.EST_VOL_EMIT] = sorted_by_site_summary.apply(
        program_output_helpers.calculate_volume_emitted, axis=1
    ).reset_index(drop=True)

    # Select only the predefined columns
    selected_sorted_by_site_summary = sorted_by_site_summary[EMIS_ESTIMATION_OUTPUT_COLUMNS]
    return (selected_sorted_by_site_summary, fugitive_emissions_to_remove)


def gen_estimated_comp_emissions_report(
    site_survey_reports_summary: pd.DataFrame,
    fugitive_emissions_rates_and_repair_dates: pd.DataFrame,
    start_date: date,
    end_date: date,
    site_ids: list[str],
    duration_factor: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generate a report of yearly estimated emissions based on only component level surveys
    Args:
        site_survey_reports (pd.DataFrame): The site survey reports
        output_dir (str): The output directory
    """
    if site_survey_reports_summary.empty:
        return

    # Filter out only the component level survey reports
    comp_reports: pd.DataFrame = site_survey_reports_summary[
        site_survey_reports_summary[eca.COMP].notnull()
    ]

    if comp_reports.empty:
        return
    
    # Get Unique measured site IDs
    unique_site_ids = comp_reports[eca.SITE_ID].unique()

    # Unique Site ID's for unmeasured sites
    unmeasured_site_ids = set(site_ids) - set(unique_site_ids)

    # Get unique combinations of site_ID, equipment and component
    unique_combinations = comp_reports[[eca.SITE_ID, eca.EQG, eca.COMP]].drop_duplicates()
    unique_site_survey_dates = comp_reports[
        [eca.SITE_ID, eca.SURVEY_COMPLETION_DATE]
    ].drop_duplicates()

    # Convert to a list of tuples
    unique_combinations_list = list(unique_combinations.itertuples(index=False, name=None))

    unique_site_survey_dates = list(unique_site_survey_dates.itertuples(index=False, name=None))

    # Create a set of tuples for all existing combinations in the DataFrame
    existing_combinations = set(
        zip(
            comp_reports[eca.SITE_ID],
            comp_reports[eca.EQG],
            comp_reports[eca.COMP],
            comp_reports[eca.SURVEY_COMPLETION_DATE],
        )
    )
    new_rows = []
    # Append unmeasured sites with zero emissions
    for site_id in unmeasured_site_ids:
        new_rows.append(
            {
                eca.SITE_ID: site_id,
                eca.EQG: None,
                eca.COMP: None,
                eca.SURVEY_COMPLETION_DATE: start_date,
                eca.M_RATE: 0,
            }
        )

    # For each site/equipment/component combination, add in the missing reports
    # for when there were no detections for a given component at a given date
    for site_id, eqg, comp in unique_combinations_list:
        # Get the unique dates for the current site_id from unique_site_survey_dates
        site_dates = set(u_date for site, u_date in unique_site_survey_dates if site == site_id)

        # Check if a date from site_dates exists for the current combination
        for s_date in site_dates:
            if (site_id, eqg, comp, s_date) not in existing_combinations:
                # If the date does not exist, add a new row with the current combination and date
                new_rows.append(
                    {
                        eca.SITE_ID: site_id,
                        eca.EQG: eqg,
                        eca.COMP: comp,
                        eca.SURVEY_COMPLETION_DATE: s_date,
                        eca.M_RATE: 0,
                    }
                )
    comp_reports = pd.concat([comp_reports, pd.DataFrame(new_rows)], ignore_index=True)
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
    comp_reports = pd.concat([comp_reports, new_data_df], ignore_index=True)

    comp_reports[eca.SURVEY_COMPLETION_DATE] = comp_reports[eca.SURVEY_COMPLETION_DATE].astype(
        "datetime64[ns]"
    )
    # Sort by the composite key - site_id, equipment, component and survey completion date
    sorted_by_site_summary = comp_reports.sort_values(
        by=[eca.SITE_ID, eca.EQG, eca.COMP, eca.SURVEY_COMPLETION_DATE]
    ).reset_index(drop=True)

    # For each unique site/equipment/component combination, calculate the days since last survey
    grouped_by_site_summary = sorted_by_site_summary.groupby([eca.SITE_ID, eca.EQG, eca.COMP])

    sorted_by_site_summary = determine_start_and_end_dates(
        sorted_by_site_summary, grouped_by_site_summary, duration_factor
    )

    fugitive_emissions_to_remove: pd.DataFrame = gen_estimated_repairable_emissions_to_remove(
        site_survey_reports_summary=sorted_by_site_summary,
        fugitive_emissions_rates_and_repair_dates=fugitive_emissions_rates_and_repair_dates,
    )

    sorted_by_site_summary[eca.EST_VOL_EMIT] = sorted_by_site_summary.apply(
        program_output_helpers.calculate_volume_emitted, axis=1
    ).reset_index(drop=True)

    return (sorted_by_site_summary, fugitive_emissions_to_remove)


def determine_start_and_end_dates(sorted_by_site_summary_df, group_by_summary, duration_factor):
    if sorted_by_site_summary_df.empty:
        return sorted_by_site_summary_df
    # Determine if the previous or next condition should be used for the emission rate
    sorted_by_site_summary_df = program_output_helpers.calculate_prev_condition(
        sorted_by_site_summary_df, group_by_summary
    )
    sorted_by_site_summary_df = program_output_helpers.calculate_next_condition(
        sorted_by_site_summary_df, group_by_summary
    )
    # Set the estimated start/end date based on the emission rate condition
    sorted_by_site_summary_df[eca.START_DATE] = (
        sorted_by_site_summary_df.groupby(eca.SITE_ID)
        .apply(
            lambda x: pd.DataFrame(
                program_output_helpers.calculate_start_date(x, duration_factor), index=x.index
            )
        )
        .reset_index(drop=True)
    )
    sorted_by_site_summary_df[eca.END_DATE] = (
        sorted_by_site_summary_df.groupby(eca.SITE_ID)
        .apply(
            lambda x: pd.DataFrame(
                program_output_helpers.calculate_end_date(x, duration_factor), index=x.index
            )
        )
        .reset_index(drop=True)
    )
    return sorted_by_site_summary_df
