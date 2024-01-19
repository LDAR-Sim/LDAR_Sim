"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        survey_planner
Purpose: The survey planner module. 

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
from scheduling.schedule_dataclasses import SiteSurveyReport
from virtual_world.sites import Site


class SurveyPlanner:
    def __init__(
        self,
        site: Site,
    ) -> None:
        self._site: Site = site
        self._active_survey_report: SiteSurveyReport = None

    def get_site(self) -> Site:
        return self._site

    def get_current_survey_report(self) -> SiteSurveyReport:
        if self._active_survey_report is None:
            self._active_survey_report = SiteSurveyReport(self._site.get_id())
            return self._active_survey_report
        else:
            return self._active_survey_report
