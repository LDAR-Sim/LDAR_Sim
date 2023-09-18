# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        out_processing.prog_table
# Purpose:     Generate output program table for web app
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

from pandas import concat, DataFrame
from out_processing.clean_results import clean_sim_df, agg_flatten


def generate(sim_results, programs):
    """ Generate output table for web app. This includes the following columns:
        'program_name', 'sim', 'emis_kg_day_site_med', 'act_leaks_day_site_med',
        'mit_vol_tco2e', 'mit_vol_perc', 'cost', 'cost_mit_vol_tco2e',
        'nat_leak_repair_count', 'emis_nat_perc'
    Args:
        sim_results (dict): simulation outputs
        baseline_program (string): Name of the Baseline program

    Returns:
        [dict]: Program summary statistics including:
            'program_name', 'sim', 'emis_kg_day_site_med', 'act_leaks_day_site_med',
            'mit_vol_tco2e', 'mit_vol_perc', 'cost', 'cost_mit_vol_tco2e',
            'nat_leak_repair_count', 'emis_nat_perc'
    """
    targ_cols_pointer = [
        '_sites_visited',
        '_eff_flags',
        '_missed_leaks',
        '_n_tags',
        '_sites_vis_w_leaks']
    out_cols_pointer = [
        '_sites_visited',
        '_eff_flags',
        '_missed_leaks',
        '_n_tags',
        '_sites_vis_w_leaks',
        '_flag_rate',
        '_tag_rate']

    ps_idx = ['program_name', 'sim']  # aggregation filter

    all_meth_cols = set()
    all_meths = set()

    # Get unique methods and unique Column names
    for pidx, p in programs.items():
        for mindx, m in p['methods'].items():
            for col in targ_cols_pointer:
                all_meth_cols.add("{}{}".format(mindx, col))
            all_meths.add(mindx)
    all_meth_cols = list(all_meth_cols)
    meth_cols = [{'in': m, 'out': m, 'type': float} for m in all_meth_cols]
    prog_ts = clean_sim_df(sim_results, 'timeseries', index='ts', params=meth_cols, aggregate=False)
    sim_stats_daily = agg_flatten(prog_ts, ps_idx, all_meth_cols,
                                  ['sum'], include_col_name=True, include_agg_name=False)
    # Calculate flag and tag rates
    for m in all_meths:
        sim_stats_daily['{}_flag_rate'.format(m)] \
            = sim_stats_daily['{}_eff_flags'.format(m)] \
            / sim_stats_daily['{}_sites_visited'.format(m)]
        sim_stats_daily['{}_tag_rate'.format(m)] \
            = sim_stats_daily['{}_sites_vis_w_leaks'.format(m)] \
            / sim_stats_daily['{}_sites_visited'.format(m)]

    # Average across all sims
    stats_daily = agg_flatten(sim_stats_daily, ['program_name'], agg_types=['mean'],
                              include_col_name=True, include_agg_name=False)

    # Separate programs into new tables where each row is a method
    prog_table = {}
    for pidx, p in programs.items():
        targ_rows = stats_daily[stats_daily['program_name'] == pidx]
        meth_table = {}
        for mindx, m in p['methods'].items():
            # Get rows that include the method label

            meth_rows = targ_rows[["{}{}".format(mindx, col) for col in out_cols_pointer]]
            meth_rows.columns = meth_rows.columns.str.replace("{}_".format(mindx), '')
            meth_rows = meth_rows.rename(columns={"eff_flags": "n_flags"})
            meth_rows['method_name'] = mindx
            meth_rows = meth_rows.set_index('method_name', drop=False)
            meth_rows = meth_rows.drop(columns=["sites_vis_w_leaks"])
            # If the method is capable of tagging, set flag-based columns to N/A
            if m['measurement_scale'] == "component":
                meth_rows['n_flags'] = "N/A"
                meth_rows['flag_rate'] = "N/A"
            else:
                meth_rows['n_tags'] = "N/A"
                meth_rows['tag_rate'] = "N/A"
            if m['is_follow_up']:
                meth_rows['prescribed_surveys'] = 'N/A'
            else:
                # This needs to be updated!
                meth_rows['prescribed_surveys'] = meth_rows['sites_visited']
            meth_table.update({mindx: meth_rows})
        if len(meth_table) > 0:
            meth_df = concat([m for _, m in meth_table.items()])
        else:
            # If there are no methods add default columns
            meth_df = DataFrame(columns=[s[1:] for s in targ_cols_pointer])

        prog_table.update({pidx: meth_df.to_dict('index')})

    return prog_table
