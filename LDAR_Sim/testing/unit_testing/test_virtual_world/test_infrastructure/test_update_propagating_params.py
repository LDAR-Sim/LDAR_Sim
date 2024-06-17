"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_update_propagating_params
Purpose: Contains unit tests for updating the propagating parameters

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

import copy
from typing import Tuple
import pandas as pd
from src.virtual_world.infrastructure import Infrastructure

from hypothesis import given, strategies as st

from src.constants.infrastructure_const import (
    Infrastructure_Constants,
    Virtual_World_To_Prop_Params_Mapping,
)
from src.constants.param_default_const import Common_Params as cp


@st.composite
def gen_methods(draw):
    methods = draw(st.lists(st.text(min_size=5, max_size=15), min_size=1))
    return methods


@st.composite
def generate_test_prop_params(draw, methods):
    to_ret = {}
    for key in Virtual_World_To_Prop_Params_Mapping.PROPAGATING_PARAMS.keys():
        to_ret[key] = draw(st.integers(min_value=0, max_value=10000))
    to_ret[cp.METH_SPECIFIC] = {}
    for key in Virtual_World_To_Prop_Params_Mapping.METH_SPEC_PROP_PARAMS.keys():
        to_ret[cp.METH_SPECIFIC][key] = {}
        for method in methods:
            to_ret[cp.METH_SPECIFIC][key][method] = draw(st.integers(min_value=0, max_value=10000))
    to_ret[cp.METH_SPECIFIC][
        Infrastructure_Constants.Sites_File_Constants.SITE_DEPLOYMENT_PLACEHOLDER
    ] = {}
    for method in methods:
        to_ret[cp.METH_SPECIFIC][
            Infrastructure_Constants.Sites_File_Constants.SITE_DEPLOYMENT_PLACEHOLDER
        ][method] = {}
    return to_ret


@st.composite
def generate_test_site_info(draw, methods):
    to_ret = {}
    for param in Infrastructure_Constants.Sites_File_Constants.PROPAGATING_PARAMS:
        param_exists = draw(st.booleans())
        if param_exists:
            if param == Infrastructure_Constants.Sites_File_Constants.SITE_DEPLOYMENT_PLACEHOLDER:
                to_ret[param] = draw(st.booleans())
            else:
                to_ret[param] = draw(st.integers(min_value=0, max_value=10000))
    for method in methods:
        for meth_param in Infrastructure_Constants.Sites_File_Constants.METH_SPEC_PROP_PARAMS:
            meth_param_exists = draw(st.booleans())
            if meth_param_exists:
                acess_key = "".join([method, meth_param])
                if (
                    meth_param
                    == Infrastructure_Constants.Sites_File_Constants.SITE_DEPLOYMENT_PLACEHOLDER
                ):
                    to_ret[acess_key] = draw(st.booleans())
                else:
                    to_ret[acess_key] = draw(st.integers(min_value=0, max_value=10000))
    return pd.Series(to_ret)


@st.composite
def generate_test_site_type_info(draw, methods):
    to_ret = {}
    for param in Infrastructure_Constants.Site_Type_File_Constants.PROPAGATING_PARAMS:
        param_exists = draw(st.booleans())
        if param_exists:
            if (
                param
                == Infrastructure_Constants.Site_Type_File_Constants.SITE_DEPLOYMENT_PLACEHOLDER
            ):
                to_ret[param] = draw(st.booleans())
            else:
                to_ret[param] = draw(st.integers(min_value=0, max_value=10000))
    for method in methods:
        for meth_param in Infrastructure_Constants.Site_Type_File_Constants.METH_SPEC_PROP_PARAMS:
            meth_param_exists = draw(st.booleans())
            if meth_param_exists:
                acess_key = "".join([method, meth_param])
                if (
                    meth_param
                    == Infrastructure_Constants.Site_Type_File_Constants.SITE_DEPLOYMENT_PLACEHOLDER
                ):
                    to_ret[acess_key] = draw(st.booleans())
                else:
                    to_ret[acess_key] = draw(st.integers(min_value=0, max_value=10000))
    return pd.Series(to_ret)


@st.composite
def generate_test_data(draw):
    methods = draw(gen_methods())
    prop_params = draw(generate_test_prop_params(methods=methods))
    site_info = draw(generate_test_site_info(methods=methods))
    site_type_info = draw(generate_test_site_type_info(methods=methods))

    return methods, prop_params, site_info, site_type_info


@given(generate_test_data())
def test_000_generate_propagating_params_correctly_updates_prop_params_dict_w_only_ints(
    inputs: Tuple[list[str], dict, pd.Series, pd.Series]
):
    methods, prop_params, site_info, site_type_info = inputs
    result = copy.deepcopy(prop_params)
    infra = Infrastructure.__new__(Infrastructure)
    infra.update_propagating_params(result, site_info, site_type_info, methods)
    meth_spec_prop_params = prop_params.pop(cp.METH_SPECIFIC)

    for param in prop_params:
        if param in site_info:
            assert result[param] == site_info[param]
        elif param in site_type_info:
            assert result[param] == site_type_info[param]
        else:
            assert result[param] == prop_params[param]
    for param in meth_spec_prop_params:
        for method in methods:
            if "".join([method, param]) in site_info:
                assert (
                    result[cp.METH_SPECIFIC][param][method] == site_info["".join([method, param])]
                )
            elif "".join([method, param]) in site_type_info:
                assert (
                    result[cp.METH_SPECIFIC][param][method]
                    == site_type_info["".join([method, param])]
                )
            else:
                assert (
                    result[cp.METH_SPECIFIC][param][method] == meth_spec_prop_params[param][method]
                )
