from pathlib import Path
import pandas as pd
from utils import conversion_constants as conv_const


def gen_estimated_emissions_report(
    site_survey_reports_summary: pd.DataFrame, output_dir: Path
) -> None:
    """Generate a report of yearly estimated emissions

    Args:
        site_survey_reports (pd.DataFrame): The site survey reports
        output_dir (str): The output directory
    """
    sorted_by_site_summary = site_survey_reports_summary.sort_values(
        by=["site_id", "survey_completion_date"]
    )

    grouped_by_site_summary = sorted_by_site_summary.groupby("site_id")

    sorted_by_site_summary["days_since_last_survey"] = (
        grouped_by_site_summary["survey_completion_date"].diff().dt.days
    )
    sorted_by_site_summary["volume_emitted"] = (
        sorted_by_site_summary["days_since_last_survey"]
        * sorted_by_site_summary["site_measured_rate"]
        * conv_const.GRAMS_PER_SECOND_TO_KG_PER_DAY
    )

    result = sorted_by_site_summary.groupby("site_id")["volume_emitted"].sum().reset_index()

    result.to_csv(output_dir / "estimated_emissions.csv", index=False)
