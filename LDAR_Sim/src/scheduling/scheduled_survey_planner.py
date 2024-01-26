"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        scheduled_survey_planner
Purpose: Module for survey planner

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
from dataclasses import dataclass
from datetime import date, timedelta
import pandas as pd
import calendar
import math
import copy
from scheduling.survey_planner import SurveyPlanner
from virtual_world.sites import Site


def get_inactive_months(active) -> list[int]:
    """
    Get inactive months
    """

    # months range from 1 to 12
    all_months = set(range(1, 13))

    # Calculate inactive months
    inactive_months: list[int] = [month for month in all_months if month not in active]
    return inactive_months


class ScheduledSurveyPlanner(SurveyPlanner):
    """A class that will generate and manage survey plans for a site for a given method.
    The survey plans will dictate when the site should be queue in
    a method survey queue to be surveyed.
    """

    def __init__(
        self,
        site: Site,
        site_annual_rs: int,
        sim_start_date: date,
        sim_end_date: date,
        deployment_years: list[int],
        deployment_months: list[int],
    ) -> None:
        super().__init__(site)
        self._sim_years: list[int] = self._get_simulation_years(
            sim_start_date=sim_start_date, sim_end_date=sim_end_date
        )
        self._site_annual_rs: int = site_annual_rs
        self._deployment_months: list[int] = deployment_months
        self._set_deployment_years(deploy_yrs=deployment_years)
        self._survey_plan: dict[int, date] = self._gen_survey_plan(site_annual_rs)
        self._current_date: date = sim_start_date - timedelta(days=1)
        self._surveys_this_year: dict[int, Survey_Counter] = self._set_survey_per_year()
        self._last_survey_dates: [date] = []
        self._queued: bool = False

    def _set_deployment_years(self, deploy_yrs: list[int]):
        if deploy_yrs:
            self._deployment_years = deploy_yrs
        else:
            self._deployment_years = self._sim_years

    def _get_simulation_years(self, sim_start_date: date, sim_end_date: date) -> list[int]:
        """Takes a start and end date and returns a list of all years between the two dates.

        Args:
            sim_start_date (date): The start date.
            Expected to be earlier (chronologically) than the end date.
            sim_end_date (date): The end date.
            Expected to be later (chronologically) than the start date.

        Returns:
            list[int]: The list of years between the provided start and end date.
        """
        start_year = sim_start_date.year
        end_year = sim_end_date.year

        # If start_date is later in the year than end_date, adjust the range
        # TODO : this should throw an error?
        if sim_start_date.month > sim_end_date.month or (
            sim_start_date.month == sim_end_date.month and sim_start_date.day > sim_end_date.day
        ):
            end_year -= 1

        return list(range(start_year, end_year + 1))

    def _gen_survey_plan(
        self,
        site_annual_rs: int,
    ) -> None:
        """Will generate an surveyed plan for the given site details in the form of
        a dictionary of years, and a nested dictionaries of survey numbers and dates
        when the site should be queued to be surveyed based on the
        site annual required surveys, site minimum interval (in days) between surveys,
        and the site survey minimum interval.

        Args:
            site_annual_rs (int): Annual required surveys at the site,
            for the method this survey plan is for.
        """
        survey_plan = []

        datetime_list = self._generate_evenly_spaced_dates(self._deployment_months, site_annual_rs)
        survey_plan = [date.date() for date in datetime_list]
        return survey_plan

    def _generate_evenly_spaced_dates(self, active_months, frequency):
        """
        Will generate evenly spaced dates
        """
        # Ensure active months are sorted
        active_months.sort()

        num_active = (
            len(active_months) - 1
        )  # the -1 is because we're assuming the given month is always included
        first_month = active_months[0]
        start_date = date(2023, first_month, 1)

        # get number of days in the given month
        num_days = calendar.monthrange(2023, first_month + num_active)[1]
        end_date = date(2023, first_month + num_active, num_days)

        evenly_spaced_dates = pd.date_range(
            start=start_date, end=end_date, periods=frequency + 1, inclusive="left"
        )

        evenly_spaced_dates = evenly_spaced_dates.to_pydatetime()
        inactive_months = get_inactive_months(active_months)
        post_sd_inactive_months = [month for month in inactive_months if month > start_date.month]
        prev_inactive_count: int = 0
        for i, survey_date in enumerate(evenly_spaced_dates):
            inactive_counts: int = len(
                [month for month in post_sd_inactive_months if month <= survey_date.month]
            )
            original_month = copy.deepcopy(survey_date.month)
            diff = 0
            # check and add if theres any inactive months that are between
            # the current month and the active month
            for x, a_month in enumerate(active_months):
                if a_month == original_month:
                    break
                elif a_month > original_month:
                    diff = original_month - active_months[x - 1] - 1
                    break
            inactive_counts += prev_inactive_count
            while survey_date.month + inactive_counts in inactive_months:
                inactive_counts += 1
                prev_inactive_count += 1
            inactive_counts += diff
            days_to_add: int = math.ceil(
                30.437 * inactive_counts
            )  # TODO : calculate the actual days instead of using placeholder 30
            evenly_spaced_dates[i] += timedelta(days=days_to_add)

        return evenly_spaced_dates

    def get_survey_plan(self) -> list[date]:
        """Returns the survey_plan"""
        return self._survey_plan

    def _set_survey_per_year(self) -> dict[int, dataclass]:
        """Creates the dictionary used to check for number of surveys done each year
        Args:
            date : Simulation start date
            date : Simulation end date
        Returns:
            dict[int, list[int]] : Year : [Survey Frequency, # Surveys Done]
        """
        _surveys_this_year: dict[int, Survey_Counter] = {}
        for year in self._sim_years:
            if year in self._deployment_years:
                _surveys_this_year[year] = Survey_Counter(
                    Required_surveys=self._site_annual_rs, Surveys_done=0
                )
            else:
                _surveys_this_year[year] = Survey_Counter(Required_surveys=0, Surveys_done=0)

        return _surveys_this_year

    def update_date(self, current_date: date) -> None:
        """This method will update the internal current date of the survey plan,
        and then adjust the values of internal state variables tracking if the site
        should be queued to surveyed based on the current date, the planned survey dates
        and if the site has already been queued to be surveyed.
        """
        self._current_date = current_date

    def _check_deployable_year(self) -> bool:
        """Checks to make sure current date is a valid year to send out crews"""
        if self._current_date.year in self._deployment_years:
            return True
        return False

    def _check_deployable_month(self) -> bool:
        """Checks to make sure current date is a valid month to send out crews"""
        if self._current_date.month in self._deployment_months:
            return True
        return False

    def queue_site_for_survey(self) -> bool:
        """Method to determine if the site for which this survey plan was generated
        should be queued to be surveyed. Will return True if the site should be
        queued to be surveyed, False otherwise.

        Returns:
            bool: Boolean indicating if the site should be queued to be surveyed.
            True if the site should be queued to be surveyed, False otherwise.
        """
        if self._check_deployable_year() is False:
            return False
        if self._check_deployable_month() is False:
            return False
        elif self._queued is False and (
            self._surveys_this_year[self._current_date.year].Required_surveys
            > self._surveys_this_year[self._current_date.year].Surveys_done
        ):
            index_num = self._surveys_this_year[self._current_date.year].Surveys_done
            if (
                self._survey_plan[index_num].month,
                self._survey_plan[index_num].day,
            ) <= (self._current_date.month, self._current_date.day):
                self._queued = True
                return True
        return False

    def unflag_for_queue(self) -> None:
        """Sets the queued flagged to false, use case is for when surveys are
        done and site is no longer a part of a queue
        """
        self._queued = False
        return None

    def add_to_surveys_done(self, current_date: date) -> None:
        """Adds to the counter keeping track of the number of surveys done"""
        self._surveys_this_year[current_date.year].Surveys_done += 1  # TODO : update when dat
        self._active_survey_report = None  # TODO make sure this makes sense here
        self.unflag_for_queue()


class MobileSurveyPlanner(ScheduledSurveyPlanner):
    def __init__(
        self,
        site: Site,
        site_annual_rs: int,
        sim_start_date: date,
        sim_end_date: date,
        deployment_years: list[int],
        deployment_months: list[int],
    ):
        super().__init__(
            site=site,
            site_annual_rs=site_annual_rs,
            sim_start_date=sim_start_date,
            sim_end_date=sim_end_date,
            deployment_years=deployment_years,
            deployment_months=deployment_months,
        )


class StationarySurveyPlanner(ScheduledSurveyPlanner):
    def __init__(
        self,
        site: Site,
        site_annual_rs: int,
        sim_start_date: date,
        sim_end_date: date,
        deployment_years: list[int],
        deployment_months: list[int],
    ):
        super().__init__(
            site=site,
            site_annual_rs=site_annual_rs,
            sim_start_date=sim_start_date,
            sim_end_date=sim_end_date,
            deployment_years=deployment_years,
            deployment_months=deployment_months,
        )


@dataclass
class Survey_Counter:
    Required_surveys: int
    Surveys_done: int
