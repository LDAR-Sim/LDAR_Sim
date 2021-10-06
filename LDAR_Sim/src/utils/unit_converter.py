# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        util.unit_converter
# Purpose:     convert leak rates into different units
#
# Copyright (C) 2018-2021  Intelligent Methane Monitoring and Management System (IM3S) Group
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------


# ---------------------Conversion Dictionaries--------------------------
substances = {
    'methane': {'n': 16.04, "input": True, "output": True},
    'natural gas': {'n': 16.80, "input": True, "output": True},
    'carbon dioxide': {'n': 44.0095, "input": False, "output": True},
}

# Mass in a tonne, Or volume in a cubic meter.
in_metrics = {
    # Unit referse to either tonne or cubic meter
    "cubic meter": {
        'per_unit': 1,
        'type': 'volume',
    },
    "gram": {
        'per_unit': 1000000,
        'type': 'mass',
    },
    "kilogram": {
        'per_unit': 1000,
        'type': 'mass',
    },
    "tonne": {
        'per_unit': 1,
        'type': 'mass',
    },
    "pound": {
        'per_unit': 2204.62,
        'type': 'mass',
    },
    "cubic feet": {
        'per_unit': 35.3147,
        'type': 'volume',
    },
    "mscf": {
        'per_unit': 0.03531,
        'type': 'volume',
    },
    "liter": {
        'per_unit': 1000,
        'type': 'volume',
    }
}

out_metrics = {
    "gram": {
        'per_unit': 1000000,
        'type': 'mass',
    },
    "kilogram": {
        'per_unit': 1000,
        'type': 'mass',
    },
    "tonne": {
        'per_unit': 1,
        'type': 'mass',
    },
    "pound": {
        'per_unit': 2204.62,
        'type': 'mass',
    },
    "cubic feet": {
        'per_unit': 35.3147,
        'type': 'volume',
    },
    "liter": {
        'per_unit': 1000,
        'type': 'volume',
    },
    "cubic meter": {
        'per_unit': 1,
        'type': 'volume',
    },
    "mscf": {
        'per_unit': 0.03531,
        'type': 'volume',
    },
}

# Time in a year
increments = {
    'second': 31540000,
    'minute': 525600,
    'hour': 8760,
    'day': 365,
    'week': 52.1429,
    'month': 12,
    'year': 1,
}

temperature_units = {
    # Conversion factors to K
    'C': {
        'scale': 1,
        'offset': 273.15,
    },
    'K': {
        'scale': 1,
        'offset': 1,
    },
    'F': {
        'scale': 0.55555555556,
        'offset': 255.372222222,
    }
}

pressure_units = {
    # Conversion factors to Pa
    'kPa': {
        'scale': 1000,
        'offset': 0,
    },
    'Pa': {
        'scale': 1,
        'offset': 0,
    },
    'psi': {
        'scale': 6894.75729,
        'offset': 0,
    },
    'atm': {
        'scale': 101325,
        'offset': 0,
    },
    'mmHg': {
        'scale': 133.322,
        'offset': 0,
    }
}
# ----------------------------------------------------------------------
# ------------------------------Functions-------------------------------


def gas_convert(
        input_quantity=0, input_substance="natural gas",
        input_metric="cubic feet", input_increment="hour",
        output_substance="natural gas", output_metric="gram",
        output_increment="second",
        NG_comp=0.949, T=60, P=1,
        temperature_unit="F",
        pressure_unit="atm",
        GWP=25, carbon_price=40,
):
    """ Converts gas flow rates to different units, and time intervals

    Args:
        input_quantity (int, optional). Defaults to 0.
        input_substance (str, optional): Type of Input Gas. Defaults to "natural gas".
            options are natural gas, methane, carbon dioxide
        input_metric (str, optional): Unit of input quantity. Defaults to "cubic feet".
            options are gram, kilogram, tonnes, pounds, cubic feet, liters, cubic meters
        input_increment (str, optional): Defaults to "hour".
            options are second, minute, hour, day, month, year
        output_substance (str, optional): Type of Output Gas. Defaults to "natural gas".
            options are natural gas, methane, carbon dioxide
        output_metric (str, optional): Unit of output quantity. Defaults to "gram".
            options are gram, kilogram, tonne, pound, cubic feet, liter, cubic meter
        output_increment (str, optional). Defaults to "second".
             options are second, minute, hour, day, month, year
        NG_comp (float, optional): Natural gas methane composition. Defaults to 0.949.
        T (int, optional): Temperature. Defaults to 20.
        P (int, optional): Pressure. Defaults to 100.
        temperature_unit (str, optional). Defaults to "C".
            options are C, K, F
        pressure_unit (str, optional). Defaults to "kPa".
            options are kPa, Pa, psi, atm, mmHg
        GWP (int, optional): [description]. Defaults to 25.
        carbon_price (int, optional): [description]. Defaults to 40.

    Use:
        gas = {
            "input_quantity": 10,
            "T": 60,
            "P": 1,
            "input_substance": "natural gas",
            "input_metric": "cubic feet",
            "input_increment": "hour",
            "output_substance": "natural gas",
            "output_metric": "grams",
            "output_increment": "second",
            "temperature_unit": "F",
            "pressure_unit": "atm",
        }

        gas_out = gas_convert(**gas)

    Returns:
        Float: Converted gas quantity
    """
    input_substance = input_substance.lower()
    input_metric = input_metric.lower()
    input_increment = input_increment.lower()
    output_substance = output_substance.lower()
    output_metric = output_metric.lower()
    output_increment = output_increment.lower()

    # --- Go from input to CO2e in tonnes per year ############
    if in_metrics[input_metric]['type'] == "mass":
        in_mass_tpy = (input_quantity * increments[input_increment]) \
            / in_metrics[input_metric]['per_unit']
    elif in_metrics[input_metric]['type'] == "volume":
        P_factors = pressure_units[pressure_unit]
        P_pa = P * P_factors['scale']+P_factors['offset']
        T_factors = temperature_units[temperature_unit]
        T_K = T * T_factors['scale']+T_factors['offset']
        vol_cubic_m = input_quantity / in_metrics[input_metric]['per_unit']
        mass_g = (vol_cubic_m * P_pa * substances[input_substance]['n']) \
            / (T_K * 8.3145)
        in_mass_tpy = mass_g * increments[input_increment] / 1000000
    if input_substance == "carbon dioxide":
        CO2e_tpy = in_mass_tpy
    elif input_substance == "methane":
        CO2e_tpy = in_mass_tpy * GWP
    else:
        CO2e_tpy = in_mass_tpy * GWP * NG_comp

    # Equivelant in Cars Per Year (4.6 Tonnes / Year)
    # CO2e_cpy = CO2e_tpy/4.6

    # ----  Now reverse the dance, back to the future! #####
    output_quantity = None
    if output_substance == "carbon dioxide":
        out_mass_tpy = CO2e_tpy
    elif output_substance == "methane":
        out_mass_tpy = CO2e_tpy / GWP
    else:
        out_mass_tpy = CO2e_tpy / GWP / NG_comp

    if out_metrics[output_metric]['type'] == "mass":
        output_quantity = out_mass_tpy \
            * out_metrics[output_metric]['per_unit'] \
            / increments[output_increment]
    else:
        P_factors = pressure_units[pressure_unit]
        P_pa = P * P_factors['scale']+P_factors['offset']
        T_factors = temperature_units[temperature_unit]
        T_K = T * T_factors['scale']+T_factors['offset']
        mass_g = (out_mass_tpy * 1000000) / increments[output_increment]
        vol_cubic_m = (mass_g * 8.3145 * T_K) \
            / (substances[output_substance]['n'] * P_pa)
        output_quantity = vol_cubic_m * out_metrics[output_metric]['per_unit']

    # dict = {
    #     "CO2e_tpy": CO2e_tpy,
    #     "CO2e_cpy": CO2e_cpy,
    #     "quantity": output_quantity

    # }
    return output_quantity
