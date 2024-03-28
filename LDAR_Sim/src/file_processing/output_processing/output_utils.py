from dataclasses import dataclass
from typing import Tuple, Any
from numpy import NaN
import pandas as pd


def percent_difference(a: float, b: float) -> float:
    if a == 0 and b == 0:
        return 0
    return abs(a - b) / ((a + b) / 2) * 100


def relative_difference(aquired_value: float, true_value: float) -> float:
    if true_value == 0:
        return 0
    return (aquired_value - true_value) / true_value * 100


def percentage_formatter(x: float, pos):
    x = x / 100
    return f"{x:.0%}"


def closest_future_date(date: pd.Timestamp, date_list: list[pd.Timestamp]) -> pd.Timestamp:
    return min([d for d in date_list if d > date], default=None, key=lambda x: abs(x - date))


def find_df_row_value_w_match(
    value_to_match: Any, value_col: str, return_col: str, df: pd.DataFrame
):
    return df.loc[df.loc[:, value_col] == value_to_match, return_col].values[0]


def luminance_shift(
    color: Tuple[float, float, float], factor: float = 0.3, lighten: bool = True
) -> Tuple[float, float, float]:
    if not lighten:
        factor = -factor
        return (max(color[0] + factor, 0), max(color[1] + factor, 0), max(color[2] + factor, 0))
    else:
        return (min(color[0] + factor, 1), min(color[1] + factor, 1), min(color[2] + factor, 1))


@dataclass
class TsEmisData:
    daily_emis: float = 0
    daily_emis_mit: float = 0
    daily_emis_non_mit: float = 0
    active_leaks: int = 0

    def __add__(self, other):
        if isinstance(other, TsEmisData):
            daily_emis = self.daily_emis + other.daily_emis
            daily_emis_mit = self.daily_emis_mit + other.daily_emis_mit
            daily_emis_non_mit = self.daily_emis_non_mit + other.daily_emis_non_mit
            active_leaks = self.active_leaks + other.active_leaks
            return TsEmisData(
                daily_emis=daily_emis,
                daily_emis_mit=daily_emis_mit,
                daily_emis_non_mit=daily_emis_non_mit,
                active_leaks=active_leaks,
            )
        else:
            raise ValueError("Unsupported operand type for addition")

    def __iadd__(self, other):
        if isinstance(other, TsEmisData):
            self.daily_emis += other.daily_emis
            self.daily_emis_mit += other.daily_emis_mit
            self.daily_emis_non_mit += other.daily_emis_non_mit
            self.active_leaks += other.active_leaks
            return self
        else:
            raise ValueError("Unsupported operand type for in-place addition")


@dataclass
class TsMethodData:
    method_name: str
    daily_deployment_cost: float = 0.0
    daily_tags: int = 0
    daily_flags: int = 0
    sites_visited: int = 0
    travel_time: int = 0
    survey_time: int = 0


@dataclass
class TaggingFlaggingStats:
    sites_flagged: int = NaN
    leaks_tagged: int = NaN


@dataclass
class CrewDeploymentStats:
    deployment_cost: float = 0.0
    sites_visited: int = 0
    travel_time: int = 0
    survey_time: int = 0


@dataclass
class EmisInfo:
    leaks_repaired: int = 0
    leaks_nat_repaired: int = 0
    repair_cost: int = 0
    nat_repair_cost: int = 0
    emis_expired: int = 0
