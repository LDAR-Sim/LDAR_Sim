"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_generate_propagating_params.py
Purpose: Contains unit tests for generating the propagating parameters

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

from virtual_world.infrastructure import Infrastructure
from virtual_world.infrastructure_const import (
    Virtual_World_To_Prop_Params_Mapping,
)
from hypothesis import given, strategies as st


@st.composite
def generate_test_virtual_world(draw):
    to_ret = {}
    answer = {}
    for key, value in Virtual_World_To_Prop_Params_Mapping.PROPAGATING_PARAMS.items():
        sub_dict = value.split(".")
        dict_to_edit = to_ret
        for counter, sub in enumerate(sub_dict):
            if sub not in dict_to_edit:
                dict_to_edit[sub] = {}
            if counter == len(sub_dict) - 1:
                # Use draw to generate a random integer for the most inner nested value
                dict_to_edit[sub] = draw(st.integers(min_value=0, max_value=10000))
            dict_to_edit = dict_to_edit[sub]
        answer[key] = dict_to_edit
    return to_ret, answer


@st.composite
def generate_test_methods(draw):
    to_ret = {}
    methods = draw(st.lists(st.text(min_size=5, max_size=15), min_size=1))
    answer = {}
    for key in Virtual_World_To_Prop_Params_Mapping.METH_SPEC_PROP_PARAMS.keys():
        answer[key] = {}
    for method in methods:
        to_ret[method] = {}
        for key, value in Virtual_World_To_Prop_Params_Mapping.METH_SPEC_PROP_PARAMS.items():
            sub_dict = value.split(".")
            dict_to_edit = to_ret[method]
            for counter, sub in enumerate(sub_dict):
                if sub not in dict_to_edit:
                    dict_to_edit[sub] = {}
                if counter == len(sub_dict) - 1:
                    # Use draw to generate a random integer for the most inner nested value
                    dict_to_edit[sub] = draw(st.integers(min_value=0, max_value=10000))
                dict_to_edit = dict_to_edit[sub]
            answer[key][method] = dict_to_edit
    return to_ret, answer


@given(generate_test_virtual_world(), generate_test_methods())
def test_000_generate_propagating_params_generates_correct_prop_params_dict_w_only_ints(vw, meth):
    """Test to confirm the generation of properly formatted output dictionary"""

    result = Infrastructure.generate_propagating_params(vw[0], meth[0])

    assert isinstance(result, dict)

    for key, value in vw[1].items():
        assert result[key] == value

    for key2, value2 in meth[1].items():
        assert result["Method_Specific_Params"][key2] == value2
