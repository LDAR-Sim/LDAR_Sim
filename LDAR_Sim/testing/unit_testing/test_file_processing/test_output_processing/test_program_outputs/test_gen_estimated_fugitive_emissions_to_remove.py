import pandas as pd
from file_processing.output_processing import program_output
from constants import output_file_constants


def gen_test_site_survey_reports_summary():
    return pd.DataFrame(
        {
            output_file_constants.EMIS_DATA_COL_ACCESSORS.SITE_ID: [
                1,
                1,
                1,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
            ],
            output_file_constants.EMIS_DATA_COL_ACCESSORS.M_RATE: [
                0,
                1,
                2,
                3,
                4,
                0,
                0,
                4,
                3,
                2,
                1,
                0,
            ],
            output_file_constants.EMIS_DATA_COL_ACCESSORS.SURVEY_COMPLETION_DATE: pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-30",
                    "2024-02-01",
                    "2024-05-06",
                    "2024-09-04",
                    "2024-12-31",
                    "2024-01-01",
                    "2024-01-29",
                    "2024-03-04",
                    "2024-08-09",
                    "2024-11-11",
                    "2024-12-31",
                ]
            ),
            output_file_constants.EMIS_DATA_COL_ACCESSORS.PREV_CONDITION: [
                False,
                False,
                False,
                False,
                False,
                True,
                False,
                True,
                True,
                True,
                True,
                True,
            ],
        }
    )


def gen_test_fugitive_emissions_rates_and_rep_data():
    return pd.DataFrame(
        {
            output_file_constants.EMIS_DATA_COL_ACCESSORS.SITE_ID: [2, 2],
            output_file_constants.EMIS_DATA_COL_ACCESSORS.DATE_REP_EXP: [
                "2024-03-16",
                "2024-08-26",
            ],
            output_file_constants.EMIS_DATA_COL_ACCESSORS.M_RATE: [2, 2],
        }
    )


def gen_expected_estimated_fugitive_emissions_to_remove():
    return pd.DataFrame(
        {
            output_file_constants.EMIS_DATA_COL_ACCESSORS.SITE_ID: [2, 2],
            output_file_constants.EMIS_DATA_COL_ACCESSORS.M_RATE: [2, 2],
            output_file_constants.EMIS_DATA_COL_ACCESSORS.START_DATE: pd.to_datetime(
                ["2024-03-16", "2024-08-26"]
            ),
            output_file_constants.EMIS_DATA_COL_ACCESSORS.END_DATE: pd.to_datetime(
                ["2024-08-09", "2024-11-11"]
            ),
            output_file_constants.EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT: [25228.8, 13305.6],
        }
    )


def test_gen_estimated_fugitive_emissions_to_remove_simple():
    site_survey_reports_summary: pd.DataFrame = gen_test_site_survey_reports_summary()
    fugitive_emissions_rates_and_rep_data: pd.DataFrame = (
        gen_test_fugitive_emissions_rates_and_rep_data()
    )
    est_fug_emis_to_rem: pd.Dataframe = program_output.gen_estimated_fugitive_emissions_to_remove(
        site_survey_reports_summary, fugitive_emissions_rates_and_rep_data
    )
    expected: pd.DataFrame = gen_expected_estimated_fugitive_emissions_to_remove()
    pd.testing.assert_frame_equal(est_fug_emis_to_rem, expected)
