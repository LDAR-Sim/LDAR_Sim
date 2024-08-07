"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        emissions_source_processing
Purpose: Module for processing User defined emissions sources

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

import logging
import sys
from pandas import DataFrame, read_csv, Series
from numpy.random import choice as random_sample
from scipy import stats
import json
from pathlib import WindowsPath
from dataclasses import dataclass
from numpy import exp as exponential

from utils.unit_converter import gas_convert
from constants.error_messages import Input_Processing_Messages as ipm
from constants.file_processing_const import Emissions_Source_Processing_Const as esp
import constants.general_const as gc


# TODO add support for fitting a distribution to source data
@dataclass
class EmissionsSourceInfo:
    data_use: str
    dist_type: str
    max_emission_rate: float
    unit_amount: str
    units_time: str
    source: list[float]


class EmissionsSource:
    def __init__(self, source_id: str):
        self.source_identifier = source_id

    def unit_conversion(
        self, for_conversion: float | list[float], unit_amount: str, unit_time: str
    ) -> float:
        # don't bother converting if units are already gram/second
        if unit_amount == gc.Unit_Constants.GRAM and unit_time == gc.Unit_Constants.SECOND:
            return for_conversion
        if isinstance(for_conversion, float):
            converted_val: float = gas_convert(
                input_quantity=for_conversion,
                input_metric=unit_amount,
                input_increment=unit_time,
            )
            return converted_val
        elif isinstance(for_conversion, list):
            converted_list: list[float] = []
            for val in for_conversion:
                converted_val: float = gas_convert(
                    input_quantity=val,
                    input_metric=unit_amount,
                    input_increment=unit_time,
                )
                converted_list.append(converted_val)
            return for_conversion

    def get_a_rate(self) -> float:
        return 0.0


class EmissionsSourceDist(EmissionsSource):
    def __init__(
        self,
        source_id: str,
        unit_amount: str,
        unit_time: str,
        dist_type: str,
        dist_shape: float,
        dist_scale: float,
        max_emis_rate: float,
    ):
        super().__init__(source_id=source_id)
        self._unit_amount: str = unit_amount
        self._unit_time: str = unit_time
        self._distribution: stats.rv_continuous = self.generate_distribution(
            dist_type=dist_type, dist_shape=dist_shape, dist_scale=dist_scale
        )
        self._max_emis_rate: float = max_emis_rate

    def get_a_rate(self) -> float:
        unconverted_rate: float = self._distribution.rvs()
        if unconverted_rate > self._max_emis_rate:
            unconverted_rate = self._max_emis_rate
        converted_rate: float = gas_convert(
            input_quantity=unconverted_rate,
            input_metric=self._unit_amount,
            input_increment=self._unit_time,
        )
        return converted_rate

    def generate_distribution(
        self, dist_type: str, dist_shape: str, dist_scale: str
    ) -> stats.rv_continuous:
        scale: float = float(dist_scale)
        if dist_type == gc.Dist_Constants.LOGNORM:
            scale = exponential(scale)
            dist_shape = dist_shape[0]
        # Ensure all shape values are captured
        shape: float | list[float] = json.loads(dist_shape)
        if not isinstance(shape, list):
            shape = [shape]
        dist_type_obj = getattr(stats, dist_type)
        distribution = dist_type_obj(*shape, 0, scale)
        return distribution


class EmissionsSourceSample(EmissionsSource):
    def __init__(
        self,
        source_id: str,
        unit_amount: str,
        unit_time: str,
        samples: list[str],
        max_emis_rate: float,
    ):
        super().__init__(source_id=source_id)
        numerical_samples = [float(sample) for sample in samples]
        self._samples = self.unit_conversion(
            for_conversion=numerical_samples,
            unit_amount=unit_amount,
            unit_time=unit_time,
        )
        self._max_emis_rate = self.unit_conversion(
            for_conversion=max_emis_rate, unit_amount=unit_amount, unit_time=unit_time
        )

    def get_a_rate(self) -> float:
        sample = random_sample(self._samples)
        if sample > self._max_emis_rate:
            sample = self._max_emis_rate
        return sample


def read_in_emissions_sources_file(
    inputs_path: WindowsPath,
    virtual_world: dict,
) -> None | DataFrame:
    """Get the location for the emissions sources file and read the file into a pandas DataFrame

    Args

    Returns

    """
    filename: str = virtual_world[esp.EMISSION][esp.EMISSION_FILE]
    filepath: WindowsPath = inputs_path / filename
    if filename is not None:
        emissions_sources_file = read_csv(filepath)
        return emissions_sources_file
    else:
        logger: logging.Logger = logging.getLogger(__name__)
        logger.error(ipm.MISSING_EMISSIONS_FILE_ERROR)
        sys.exit()


def process_emission_sources(
    inputs_path: WindowsPath, virtual_world: dict
) -> dict[str, EmissionsSource]:
    # Try to read in Emissions Sources file
    emissions_source_file = read_in_emissions_sources_file(
        inputs_path=inputs_path, virtual_world=virtual_world
    )
    # Read in the emissions sources file
    processed_emissions_sources: dict[str, EmissionsSource] = process_emission_source_file(
        emissions_source_file
    )

    return processed_emissions_sources


def process_emission_source_file(emis_sources: DataFrame) -> dict[str, EmissionsSource]:
    """Process the given emissions sources DataFrame in order to
    set up the correct emissions sources types.

    Emissions sources of the sample type will be set up as a list of sample values,

    Emissions sources of the fit type will be set up as a scipy distribution object,

    Emissions sources of the distribution type will be set up as a scipy distribution object.

    Args:
        emiss_source (DataFrame): _description_

    Returns:
        dict[str, (List or scipy dist obj)]: _description_
    """
    processed_emissions_data: dict[str, EmissionsSource] = {}
    for source_name in emis_sources.columns:
        clean_source_name = source_name.strip()
        emis_source_info: EmissionsSourceInfo = read_in_emis_source_col(
            source_name, emis_sources[source_name]
        )
        unit_amount: str = emis_source_info.unit_amount.strip()
        unit_time: str = emis_source_info.units_time.strip()
        if esp.DIST_REGEX.search(emis_source_info.data_use):
            emis_source: EmissionsSource = EmissionsSourceDist(
                source_id=clean_source_name,
                unit_amount=unit_amount,
                unit_time=unit_time,
                dist_type=emis_source_info.dist_type,
                dist_shape=emis_source_info.source[1:],
                dist_scale=emis_source_info.source[0],
                max_emis_rate=emis_source_info.max_emission_rate,
            )
        elif esp.SAMPLE_REGEX.search(emis_source_info.data_use):
            emis_source: EmissionsSource = EmissionsSourceSample(
                source_id=clean_source_name,
                unit_amount=unit_amount,
                unit_time=unit_time,
                samples=emis_source_info.source,
                max_emis_rate=emis_source_info.max_emission_rate,
            )
        else:
            print(ipm.INVALID_EMISSIONS_SOURCE_ERROR.format(source_name=clean_source_name))

        processed_emissions_data[clean_source_name] = emis_source

    return processed_emissions_data


def read_in_emis_source_col(column_name: str, emis_source_col: Series) -> EmissionsSourceInfo:
    # col_vals: list[str] = emis_source_col.str.split(",")
    try:
        date_use: str = emis_source_col[0]
    except Exception as e:
        print(
            ipm.INVALID_EMISSIONS_SOURCE_FILE_VALUE_ERROR.format(
                value=ipm.INVALID_EMISSIONS_VALUE["data"], source=column_name, exception=e
            )
        )
    try:
        dist_type: str = emis_source_col[1]
    except Exception as e:
        print(
            ipm.INVALID_EMISSIONS_SOURCE_FILE_VALUE_ERROR.format(
                value=ipm.INVALID_EMISSIONS_VALUE["dist"], source=column_name, exception=e
            )
        )
    try:
        max_emis_rate: float = float(emis_source_col[2])
    except Exception as e:
        print(
            ipm.INVALID_EMISSIONS_SOURCE_FILE_VALUE_ERROR.format(
                value=ipm.INVALID_EMISSIONS_VALUE["max_emis"], source=column_name, exception=e
            )
        )
    try:
        unit_amount: str = emis_source_col[3]
    except Exception as e:
        print(
            ipm.INVALID_EMISSIONS_SOURCE_FILE_VALUE_ERROR.format(
                value=ipm.INVALID_EMISSIONS_VALUE["unit_amt"], source=column_name, exception=e
            )
        )
    try:
        units_time: str = emis_source_col[4]
    except Exception as e:
        print(
            ipm.INVALID_EMISSIONS_SOURCE_FILE_VALUE_ERROR.format(
                value=ipm.INVALID_EMISSIONS_VALUE["unit_time"], source=column_name, exception=e
            )
        )
    try:
        source: list[str] = Series(emis_source_col[5:]).dropna().tolist()
    except Exception as e:
        print(
            ipm.INVALID_EMISSIONS_SOURCE_FILE_VALUE_ERROR.format(
                value=ipm.INVALID_EMISSIONS_VALUE["source"], source=column_name, exception=e
            )
        )
    return EmissionsSourceInfo(
        data_use=date_use,
        dist_type=dist_type,
        max_emission_rate=max_emis_rate,
        unit_amount=unit_amount,
        units_time=units_time,
        source=source,
    )
