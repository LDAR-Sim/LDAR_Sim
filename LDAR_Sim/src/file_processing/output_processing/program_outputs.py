from datetime import date
from pathlib import Path
import pandas as pd
from scheduling.schedule_dataclasses import SiteSurveyReport
from utils import conversion_constants as conv_const


def gen_estimated_emissions_report(
    site_survey_reports_summary: pd.DataFrame,
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

    grouped_by_site_summary = sorted_by_site_summary.groupby("site_id")

    sorted_by_site_summary["days_since_last_survey"] = (
        grouped_by_site_summary["survey_completion_date"].diff().dt.days
    )
    sorted_by_site_summary["days_until_next_survey"] = (
        grouped_by_site_summary["survey_completion_date"].diff(-1).dt.days
    )
    use_prev_condition = sorted_by_site_summary["site_measured_rate"] > sorted_by_site_summary[
        "site_measured_rate"
    ].shift(-1)
    use_next_condition = sorted_by_site_summary["site_measured_rate"] < sorted_by_site_summary[
        "site_measured_rate"
    ].shift(1)
    sorted_by_site_summary["volume_emitted"] = 0.0
    sorted_by_site_summary.loc[use_prev_condition, "volume_emitted"] += (
        sorted_by_site_summary["days_since_last_survey"]
        * sorted_by_site_summary["site_measured_rate"]
        * conv_const.GRAMS_PER_SECOND_TO_KG_PER_DAY
    )
    sorted_by_site_summary.loc[use_next_condition, "volume_emitted"] += (
        sorted_by_site_summary["days_until_next_survey"]
        * sorted_by_site_summary["site_measured_rate"]
        * conv_const.GRAMS_PER_SECOND_TO_KG_PER_DAY
    )
    sorted_by_site_summary["year"] = sorted_by_site_summary["survey_completion_date"].dt.year

    result = (
        sorted_by_site_summary.groupby(["site_id", "year"])["volume_emitted"].sum().reset_index()
    )
    filename: str = "_".join([name, "estimated_emissions.csv"])

    result.to_csv(output_dir / filename, index=False)


def gen_estimated_fugitive_emissions_to_remove(
    site_survey_reports_summary: pd.DataFrame,
    fugitive_emissions_rates_and_repair_dates: pd.DataFrame,
    start_date: date,
    end_date: date,
) -> dict[str, float]:
    """
    Generate a report of yearly estimated fugitive emissions to remove to avoid double counting
    """
    fugitve_emissions_per_year_to_remove = {}
    if site_survey_reports_summary.empty:
        return fugitve_emissions_per_year_to_remove
    return fugitve_emissions_per_year_to_remove
