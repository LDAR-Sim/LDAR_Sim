# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        utils.sensitivity
# Purpose:     Handle sensitivity functions
#
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

import copy

import matplotlib.pyplot as plt
import yaml


def yaml_to_dict(y_file):
    """Convert a Yaml file to a dictionary

    Args:
        y_file (string): Yaml filepath

    Returns:
        dict: Yaml converted to dictionary
    """
    with open(y_file, "r") as f_content:
        try:
            return yaml.safe_load(f_content)
        except yaml.YAMLError as exc:
            print(exc)


def generate_sens_prog_set(sens_z_var, programs):
    """Generate a program set of sensitivity programs using
        a range of values for the parameter.

    Args:
        sens_z_var (dict): Must include two key-list sets:
             path - List of paths to variable. eg.  P_Air.methods.air.sensor.MDL
             vals - List of values associated with the param. eg [0, 1, 2, 3]

        programs (dict): program object

    Returns:
        dict: updated program object
    """
    new_progs = []
    prev_progs_names = set()
    if sens_z_var:
        # Go through sensitivity progs
        var_paths = [path.split(".") for path in sens_z_var["paths"]]
        # Get program names and their associated index in programs object
        key = var_paths[0][-1]
        for val in sens_z_var["vals"]:
            for path in var_paths:
                for pidx, p in enumerate(programs):
                    if p["program_name"] == path[0] or path[0].lower() == "__all":
                        prev_progs_names.add(path[0])
                        tmp_prog = copy.deepcopy(programs[pidx])
                        set_from_keylist(tmp_prog, path[1:], val)

                        tmp_prog["orig_program_name"] = tmp_prog["program_name"]
                        tmp_prog["program_name"] = "_".join(
                            [str(elem) for elem in path if str(elem) != "methods"] + [str(val)]
                        )
                new_progs.append(tmp_prog)
        for prog in list(prev_progs_names):
            prog_idx = next(
                (idx for (idx, p) in enumerate(programs) if p["program_name"] == prog),
                None,
            )
            programs.pop(prog_idx)
    programs += new_progs
    for prog in programs:
        if "orig_program_name" not in prog:
            prog["orig_program_name"] = prog["program_name"]
        if sens_z_var:
            prog["value_z"], prog["key_z"] = val, key
    return programs


def set_from_keylist(dic, keys, value):
    """Update program value sensitivity keys (variable path) and value.
        keys are a hierarchical path to variable.

             program     method       variable
               |            |  vargroup  |
               |            |    |       |
        eg.  [P_Air,methods.Air,cost,per_site]
        or
            program             variable
               |    vargroup       |
               |       |           |
        eg.  [P_Air,emissions,max_leak_rate]
    Args:
        dic (dict): input is program, internal is current dict object
        keys (list): path to variable (see above)
        value : Value of variable
    """
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def group_timeseries(time_series, group_col):
    groups = {}
    for pname in list(time_series.program_name.unique()):
        for val in list(time_series[group_col].unique()):
            groups.update(
                {
                    "{}_{}".format(pname, val): time_series[
                        (time_series.program_name == pname) & (time_series[group_col] == val)
                    ]
                }
            )
    return groups


def generate_violin(grouped_ts, val_col, y_label, output_dir):
    # Turn interactive plotting off
    plt.ioff()
    outdata = [list(prog[val_col]) for pdix, prog in grouped_ts.items()]
    textstr = "\n".join(["{}. {}".format(pidx + 1, pname) for pidx, pname in enumerate(grouped_ts)])
    fig, ax = plt.subplots()
    ax.set_xlabel("program")
    ax.set_ylabel(y_label)
    ax.violinplot(outdata, widths=0.7, showmeans=True, showextrema=True, showmedians=True)
    ax.set_xticks([i + 1 for i in range(len(grouped_ts))])
    ax.text(
        0.05,
        0.95,
        textstr,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox={"boxstyle": "round", "alpha": 0.3, "color": "orangered"},
    )
    fig.tight_layout()
    fig.savefig(output_dir / "violin_{}".format(val_col), dpi=fig.dpi)
    plt.close(fig)
