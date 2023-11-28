from datetime import datetime, timedelta


from initialization.sites import Site


class SurveyPlanner:
    """A class that will generate and manage survey plans for a site for a given method.
    The survey plans will dictate when the site should be queue in
    a method survey queue to be surveyed.
    """

    def __init__(
        self,
        site: Site,
        site_annual_rs: int,
        sim_start_date: datetime,
        sim_end_date: datetime,
        deployment_years: list[int],
        deployment_months: list[int],
    ) -> None:
        sim_years: list[int] = self.get_simulation_years(
            sim_start_date=sim_start_date, sim_end_date=sim_end_date
        )
        self._deployment_months: list[int] = deployment_months
        self._deployment_years: list[int] = deployment_years
        self._gen_survey_plan(sim_years, site_annual_rs)
        self._current_date: datetime = sim_start_date
        self._surveys_this_year: dict[str, int] = {}
        self._last_survey_dates: dict[str, datetime] = {}

    def get_simulation_years(self, sim_start_date: datetime, sim_end_date: datetime) -> list[int]:
        """Takes a start and end date and returns a list of all years between the two dates.

        Args:
            sim_start_date (datetime): The start date.
            Expected to be earlier (chronologically) than the end date.
            sim_end_date (datetime): The end date.
            Expected to be later (chronologically) than the start date.

        Returns:
            list[int]: The list of years between the provided start and end date.
        """
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
        """Will generate an surveyed plan for the given site details in the form of
        a dictionary of years, and a nested dictionaries of survey numbers and dates
        when the site should be queued to be surveyed based on the
        site annual required surveys, site minimum interval (in days) between surveys,
        and the site survey minimum interval.

        Args:
            sim_years (list[int]): The list of active years to generate the survey plan for.
            site_annual_rs (int): Annual required surveys at the site,
            for the method this survey plan is for.
            site_survey_min_int (int): The minimum interval between surveys.
            site_min_time_bt_surveys (int): The minimum time between surveys in days.
        """
        self._survey_plan: dict[str, dict[str, datetime]] = {}
        for year in sim_years:
            if year in self._deployment_years:
                self._survey_plan[year] = self._gen_yearly_survey_plan(
                    site_annual_rs=site_annual_rs,
                    site_survey_min_int=site_survey_min_int,
                    site_min_time_bt_surveys=site_min_time_bt_surveys,
                )

    def update(self) -> None:
        """This method will update the internal current date of the survey plan,
        and then adjust the values of internal state variables tracking if the site
        should be queued to surveyed based on the current date, the planned survey dates
        and if the site has already been queued to be surveyed.
        """
        self._current_date += timedelta(days=1)

    def queue_site_for_survey() -> bool:
        """Method to determine if the site for which this survey plan was generated
        should be queued to be surveyed. Will return True if the site should be
        queued to be surveyed, False otherwise.

        Returns:
            bool: Boolean indicating if the site should be queued to be surveyed.
            True if the site should be queued to be surveyed, False otherwise.
        """
        return False
