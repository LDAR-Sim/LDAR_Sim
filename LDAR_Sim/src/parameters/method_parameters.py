from typing import Any
from constants import param_default_const


class SensorParameters:
    def __init__(self, sensor_params: dict[str, Any]) -> None:
        self._type: str = sensor_params[param_default_const.Method_Params.TYPE]
        self._quantification_error: float = sensor_params[param_default_const.Method_Params.QE]
        self._mdl: list[float] | float = sensor_params[param_default_const.Method_Params.MDL]
        self._mod_loc: str = sensor_params[param_default_const.Method_Params.MOD_LOC]


class CoverageParameters:
    def __init__(self, coverage_params: dict[str, Any]) -> None:
        self._spatial: float = coverage_params[param_default_const.Method_Params.SPATIAL]
        self._temporal: float = coverage_params[param_default_const.Method_Params.TEMPORAL]


class CostParameters:
    def __init__(self, cost_params: dict[str, Any]) -> None:
        if (
            cost_params[param_default_const.Method_Params.COST][
                param_default_const.Method_Params.PER_DAY
            ]
            == 0
        ):
            self._cost: float = cost_params[param_default_const.Method_Params.COST][
                param_default_const.Method_Params.PER_DAY
            ]
        else:
            self._cost: float = cost_params[param_default_const.Method_Params.COST][
                param_default_const.Method_Params.PER_SITE
            ]
        self._upfront_cost: float = cost_params[param_default_const.Method_Params.COST][
            param_default_const.Method_Params.UPFRONT
        ]


class TravelTimeParameters:
    def __init__(self, travel_time_params: dict[str, Any]) -> None:
        if travel_time_params[param_default_const.Common_Params.FILE] is None:
            self._travel_time: list[float] = travel_time_params[
                param_default_const.Common_Params.VAL
            ]
            self._use_file: bool = False
        else:
            self._travel_time_file: str = travel_time_params[param_default_const.Common_Params.FILE]
            self._use_file: bool = True


class SchedulingParameters:
    def __init__(self, scheduling_params: dict[str, Any]) -> None:
        self._deployment_month: list[int] = scheduling_params[
            param_default_const.Method_Params.DEPLOYMENT_MONTHS
        ]
        self._deployment_years: list[int] = scheduling_params[
            param_default_const.Method_Params.DEPLOYMENT_YEARS
        ]
        self._min_time_bt_surveys: int = scheduling_params[
            param_default_const.Method_Params.MIN_TIME_BT_SURVEYS
        ]


class WeatherEnvelopeParameters:
    def __init__(self, weather_envelope_params: dict[str, Any]) -> None:
        self._precipitation_min: float = weather_envelope_params[
            param_default_const.Method_Params.PRECIP
        ][0]
        self._precipitation_max: float = weather_envelope_params[
            param_default_const.Method_Params.PRECIP
        ][1]
        self._temperature_min: float = weather_envelope_params[
            param_default_const.Method_Params.TEMP
        ][0]
        self._temperature_max: float = weather_envelope_params[
            param_default_const.Method_Params.TEMP
        ][1]
        self._wind_speed_min: float = weather_envelope_params[
            param_default_const.Method_Params.WIND
        ][0]
        self._wind_speed_max: float = weather_envelope_params[
            param_default_const.Method_Params.WIND
        ][1]


class FollowUpParameters:
    def __init__(self, follow_up_params: dict[str, Any]) -> None:
        self._preferred_method: str = follow_up_params[
            param_default_const.Method_Params.PREFERRED_METHOD
        ]
        self._delay: int = follow_up_params[param_default_const.Method_Params.DELAY]
        self._instant_threshold: float = follow_up_params[
            param_default_const.Method_Params.INSTANT_THRESHOLD
        ]
        self._instant_threshold_type: str = follow_up_params[
            param_default_const.Method_Params.INSTANT_THRESHOLD_TYPE
        ]
        self._interaction_priority: str = follow_up_params[
            param_default_const.Method_Params.INTERACTION_PRIORITY
        ]
        self._proportion: float = follow_up_params[param_default_const.Method_Params.PROPORTION]
        self._redundancy_filter: str = follow_up_params[
            param_default_const.Method_Params.REDUNDANCY_FILTER
        ]
        self._sort_by_rate: bool = follow_up_params[param_default_const.Method_Params.SORT_BY_RATE]
        self._threshold: float = follow_up_params[param_default_const.Method_Params.THRESHOLD]
        self._threshold_type: str = follow_up_params[
            param_default_const.Method_Params.THRESHOLD_TYPE
        ]


class MethodParameters:
    def __init__(self, methods: dict[str, Any]) -> None:
        self._version: str = methods[param_default_const.Common_Params.VERSION]
        self._parameter_level: str = methods[param_default_const.Levels.METHOD]
        self._name: str = methods[param_default_const.Method_Params.NAME]
        self._measurement_scale: str = methods[param_default_const.Method_Params.MEASUREMENT_SCALE]
        self._deployment_type: str = methods[param_default_const.Method_Params.DEPLOYMENT_TYPE]
        self._sensor: SensorParameters = SensorParameters(
            methods[param_default_const.Method_Params.SENSOR]
        )
        self._coverage: CoverageParameters = CoverageParameters(
            methods[param_default_const.Method_Params.COVERAGE]
        )
        self._costs: CostParameters = CostParameters(
            methods[param_default_const.Method_Params.COST]
        )
        self._crew_count: int = methods[param_default_const.Method_Params.N_CREWS]
        self._consider_daylight: bool = methods[param_default_const.Method_Params.CONSIDER_DAYLIGHT]
        self._survey_frequency: int = methods[param_default_const.Method_Params.RS]
        self._survey_time: int = methods[param_default_const.Method_Params.TIME]
        self._max_work_hours: int = methods[param_default_const.Method_Params.MAX_WORKDAY]
        self._reporting_delay: int = methods[param_default_const.Method_Params.REPORTING_DELAY]
        self._travel_time: TravelTimeParameters = TravelTimeParameters(
            methods[param_default_const.Method_Params.T_BW_SITES]
        )
        self._scheduling: SchedulingParameters = SchedulingParameters(
            methods[param_default_const.Method_Params.SCHEDULING]
        )
        self._weather_envelope: WeatherEnvelopeParameters = WeatherEnvelopeParameters(
            methods[param_default_const.Method_Params.WEATHER_ENVS]
        )
        self._is_follow_up: bool = methods[param_default_const.Method_Params.IS_FOLLOW_UP]
        self._follow_up_info: FollowUpParameters = FollowUpParameters(
            methods[param_default_const.Method_Params.FOLLOW_UP]
        )
