from datetime import datetime, timedelta


class SurveyPlanner:
    def __init__(
        self,
        sim_start_date: datetime,
        sim_end_date: datetime,
        site_annual_rs: int,
        site_survey_min_int: int,
        site_min_time_bt_surveys: int,
        deployment_years: list[int],
        deployment_months: list[int],
    ) -> None:
        sim_years: list[int] = self.get_simulation_years(
            sim_start_date=sim_start_date, sim_end_date=sim_end_date
        )
        self._deployment_months: list[int] = deployment_months
        self._deployment_years: list[int] = deployment_years
        self._gen_survey_plan(
            sim_years, site_annual_rs, site_survey_min_int, site_min_time_bt_surveys
        )
        self._current_date: datetime = sim_start_date

    def get_simulation_years(self, sim_start_date: datetime, sim_end_date: datetime) -> list[int]:
        sim_years: list[int] = []
        curr_date: datetime = sim_start_date
        while curr_date <= sim_end_date:
            sim_years.append(curr_date.year)
            curr_date += timedelta(days=365)
        return sim_years

    def _gen_survey_plan(
        self,
        sim_years: list[int],
        site_annual_rs: int,
        site_survey_min_int: int,
        site_min_time_bt_surveys: int,
    ) -> None:
        self._survey_plan: dict[str, dict[str, datetime]] = {}
        for year in sim_years:
            if year in self._deployment_years:
                self._survey_plan[year] = self._gen_yearly_survey_plan(
                    site_annual_rs=site_annual_rs,
                    site_survey_min_int=site_survey_min_int,
                    site_min_time_bt_surveys=site_min_time_bt_surveys,
                )

    def _gen_yearly_survey_plan(
        self,
        site_annual_rs: int,
        site_survey_min_int: int,
        site_min_time_bt_surveys: int,
    ) -> dict[str, datetime]:
        return

    def update(self) -> None:
        self._current_date += timedelta(days=1)
