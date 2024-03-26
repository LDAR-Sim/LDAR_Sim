from datetime import date
from pathlib import Path
import pandas as pd
from scheduling.schedule_dataclasses import SiteSurveyReport
from utils import conversion_constants as conv_const
from file_processing.output_processing import output_constants
from file_processing.output_processing import output_utils


def gen_estimated_emissions_report(
    site_survey_reports_summary: pd.DataFrame,
    fugutive_emissions_rates_and_repair_dates: pd.DataFrame,
    output_dir: Path,
    name: str,
    start_date: date,
    end_date: date,
) -> None:
    """Generate a report of yearly estimated emissions

    Args:
        site_survey_reports (pd.DataFrame): The site survey reports
        output_dir (str): The output directory
    """
    if site_survey_reports_summary.empty:
        return

    site_ids: list = site_survey_reports_summary["site_id"].unique()

    for site_id in site_ids:

        site_survey_reports_summary.loc[len(site_survey_reports_summary)] = SiteSurveyReport(
            site_id=site_id, survey_start_date=start_date, survey_completion_date=start_date
        ).to_report_summary()

        site_survey_reports_summary.loc[len(site_survey_reports_summary)] = SiteSurveyReport(
            site_id=site_id, survey_start_date=end_date, survey_completion_date=end_date
        ).to_report_summary()

    site_survey_reports_summary["survey_completion_date"] = site_survey_reports_summary[
        "survey_completion_date"
    ].astype("datetime64[ns]")

    sorted_by_site_summary = site_survey_reports_summary.sort_values(
        by=["site_id", "survey_completion_date"]
    )

    fugitive_emissions_to_remove: pd.DataFrame = gen_estimated_fugitive_emissions_to_remove(
        sorted_by_site_summary, fugutive_emissions_rates_and_repair_dates
    )

    grouped_by_site_summary = sorted_by_site_summary.groupby("site_id")

    sorted_by_site_summary["days_since_last_survey"] = (
        grouped_by_site_summary["survey_completion_date"].diff().dt.days
    )
    sorted_by_site_summary["days_until_next_survey"] = abs(
        grouped_by_site_summary["survey_completion_date"].diff(-1).dt.days
    )
    sorted_by_site_summary["use_prev_condition"] = (
        grouped_by_site_summary["site_measured_rate"].diff() < 0
    )
    sorted_by_site_summary["use_next_condition"] = (
        grouped_by_site_summary["site_measured_rate"].diff(-1) < 0
    )
    sorted_by_site_summary["volume_emitted"] = 0.0
    sorted_by_site_summary.loc[sorted_by_site_summary["use_prev_condition"], "volume_emitted"] += (
        sorted_by_site_summary["days_since_last_survey"]
        * sorted_by_site_summary["site_measured_rate"].shift(1)
        * conv_const.GRAMS_PER_SECOND_TO_KG_PER_DAY
    )
    sorted_by_site_summary.loc[sorted_by_site_summary["use_next_condition"], "volume_emitted"] += (
        sorted_by_site_summary["days_until_next_survey"]
        * sorted_by_site_summary["site_measured_rate"].shift(-1)
        * conv_const.GRAMS_PER_SECOND_TO_KG_PER_DAY
    )
    sorted_by_site_summary["year"] = sorted_by_site_summary["survey_completion_date"].dt.year

    result = (
        sorted_by_site_summary.groupby(["site_id", "year"])["volume_emitted"].sum().reset_index()
    )

    if not fugitive_emissions_to_remove.empty:
        final_result: pd.DataFrame = result - fugitive_emissions_to_remove
    else:
        final_result = result

    filename: str = "_".join([name, "estimated_emissions.csv"])

    final_result.to_csv(output_dir / filename, index=False)


def gen_estimated_fugitive_emissions_to_remove(
    site_survey_reports_summary: pd.DataFrame,
    fugitive_emissions_rates_and_repair_dates: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate a report of yearly estimated fugitive emissions to remove to avoid double counting
    """
    if fugitive_emissions_rates_and_repair_dates.empty:
        return pd.DataFrame()
    # Switch the data types of the repair date column to datetime so date computations can be done
    fugitive_emissions_rates_and_repair_dates[output_constants.EMIS_DATA_COL_ACCESSORS.DATE_REP] = (
        fugitive_emissions_rates_and_repair_dates[
            output_constants.EMIS_DATA_COL_ACCESSORS.DATE_REP
        ].astype("datetime64[ns]")
    )

    # Populate a new column in the fugitive emissions rates and repair dates dataframe
    # with the closest future survey date. This wil be used to compute the estimated
    # fugitive emissions to remove to avoid double counting
    fugitive_emissions_rates_and_repair_dates[
        "closest_survey_date"
    ] = fugitive_emissions_rates_and_repair_dates[
        output_constants.EMIS_DATA_COL_ACCESSORS.DATE_REP
    ].apply(
        lambda x: output_utils.closest_future_date(
            x, site_survey_reports_summary["survey_completion_date"].unique()
        )
    )
    # Calculate the estimated fugitive emissions that took place between the repair date
    # and the next survey date. This is what we will remove to avoid double counting.
    fugitive_emissions_rates_and_repair_dates["fugitive_emissions_to_remove"] = (
        fugitive_emissions_rates_and_repair_dates[output_constants.EMIS_DATA_COL_ACCESSORS.M_RATE]
        * conv_const.GRAMS_PER_SECOND_TO_KG_PER_DAY
        * (
            fugitive_emissions_rates_and_repair_dates["closest_survey_date"]
            - fugitive_emissions_rates_and_repair_dates[
                output_constants.EMIS_DATA_COL_ACCESSORS.DATE_REP
            ]
        ).dt.days
    )

    # Add in the year of occurence
    fugitive_emissions_rates_and_repair_dates["year"] = fugitive_emissions_rates_and_repair_dates[
        "closest_survey_date"
    ].dt.year

    # Group by sites and year and sum
    result = (
        fugitive_emissions_rates_and_repair_dates.groupby(
            [output_constants.EMIS_DATA_COL_ACCESSORS.SITE_ID, "year"]
        )["fugitive_emissions_to_remove"]
        .sum()
        .reset_index()
    )

    return result
