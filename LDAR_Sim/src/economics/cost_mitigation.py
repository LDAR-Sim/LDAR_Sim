# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        economics.cost_mitigation
# Purpose:     Creates outputs across multiple programs and simulations
#
# Copyright (C) 2018-2021
# Intelligent Methane Monitoring and Management System (IM3S) Group
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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def cost_mitigation(simulation_dfs, ref_program, no_program, output_directory):
    """This function takes the simulation dataframes and economics
    default program parameters as inputs. It calculates the cost
    of each LDAR program and breaks each down into individual
    method costs before averaging the costs annually per site.
    It also calculates the amount of gas each program mitigates
    below the baseline program (no LDAR) and determines the value
    of captured gas if sold. Using this value and the costs, the
    function calculates a cost/mitigation ratio. Outputs are two
    figures: one for the costs/method/site and the other plots
    the cost/mitigation ratios of each program. Two csv files
    are also output into the file directory.
    """

    # Get simulation dataframes and put them in a dictionary, convert to df.
    economics_outputs = [{
        'program_name': df['program_name'],
        'total_program_emissions_kg':
        df['timeseries']['daily_emissions_kg'].sum(),
        'sale_price_natgas': df['p_params']['economics']['sale_price_natgas'],
        'GWP_CH4': df['p_params']['economics']['GWP_CH4'],
        'carbon_price_tonnesCO2e':
        df['p_params']['economics']['carbon_price_tonnesCO2e'],
        'social_cost_CH4_tonnes':
        df['p_params']['economics']['social_cost_CH4_tonnes'],
        'cost_CCUS': df['p_params']['economics']['cost_CCUS'],
        'cost_low_bleed_pneu_tCO2e':
        df['p_params']['economics']['cost_low_bleed_pneu_tCO2e'],
        'total_program_cost': df['timeseries']['total_daily_cost'].sum()
    } for df in simulation_dfs]

    economics_outputs_df = pd.DataFrame(economics_outputs)

    # Need to verify if P_none was input or economics module will not work.
    if 'P_none' in economics_outputs_df.values:
        print("P_none input. Economics functionality running.")
    else:
        raise Exception("No P_none input. Cannot run economics.")

    # Calculate the mean emissions and costs accross all sims, convert units.
    economics_df = economics_outputs_df.groupby(by='program_name').mean()

    economics_df['total_emissions_mcf'] = (
        ((economics_df['total_program_emissions_kg']
            / 0.678) * 35.3147) / 1000)

    economics_df['simulation_avg_emissions_tonnesCO2e'] = (
        (economics_df['total_program_emissions_kg'] / 1000) *
        economics_df['GWP_CH4'])

    # Find the simulation average emissions from the base program (no LDAR).
    # Subtract from programs.
    P_none_value = economics_df.loc['P_none', 'total_emissions_mcf']

    economics_df['difference_none_mcf'] = (
        economics_df['total_emissions_mcf'] - P_none_value)

    # Take difference in emissions and multiply by sale price of natural gas.
    # Check to make sure Alt-Program achieves reductions over P_none.
    for row in economics_df['difference_none_mcf']:
        if row <= 0:
            economics_df['value_gas_sold'] = (
                abs(economics_df['difference_none_mcf']) *
                economics_df['sale_price_natgas'])
        else:
            economics_df['value_gas_sold'] = 0

    # Find difference from baseline (no LDAR) in tonnes CO2e.
    # Use value for cost/mitigation ratio.
    # Need to verify that alt-program(s) achieve reductions over baseline.
    for row in economics_df['difference_none_mcf']:
        if row <= 0:
            economics_df['dif_none_tonnesCO2e'] = (
                ((((abs(
                    economics_df['difference_none_mcf'])
                    * 1000) / 35.3147) * 0.678) / 1000) *
                economics_df['GWP_CH4'])

        else:
            economics_df['dif_none_tonnesCO2e'] = 0

    economics_df['cost_mitigation_ratio'] = np.divide(
        economics_df['total_program_cost'],
        economics_df['dif_none_tonnesCO2e'],
        out=np.zeros_like(
            economics_df['total_program_cost']),
        where=economics_df['dif_none_tonnesCO2e'] != 0)

    # Reset index of df and set up program list and x ticks for plotting.
    economics_df.reset_index(inplace=True)
    programs = economics_df['program_name']
    x = np.arange(len(programs))

    # Plot up the cost mitigation ratios for each program and comparables.
    plt.xticks(x, programs)
    plt.scatter(x, economics_df['cost_mitigation_ratio'], marker='o',
                c=np.random.rand(len(x)), s=100),
    plt.axhline(y=economics_df['carbon_price_tonnesCO2e'][1],
                color="darkgreen", linestyle='dashed', label="Carbon Price"),
    plt.axhline(y=economics_df['cost_CCUS'][1], color='blue',
                linestyle='dotted', label='Cost CCUS (Pure Stream)'),
    plt.ylabel("$/tonne CO2e"),
    plt.xlabel("Program"),
    plt.title("Comparing LDAR Program Cost Mitigation Ratios"),
    plt.legend(),
    plt.savefig(output_directory / 'cost_mitigation_plot.png')

    # Set up number of sites and timesteps for cost/method/site plot.
    n_sites = len(simulation_dfs[0]['sites'])
    timesteps = len(simulation_dfs[0]['timeseries'])

    # Get costs from other df's into new df.
    df1 = pd.DataFrame(df['timeseries'].filter(regex='cost$', axis=1).sum()
                       for df in simulation_dfs)
    df1['program_name'] = [df['program_name'] for df in simulation_dfs]
    cost_df = df1.groupby(by='program_name').mean()
    cost_df.reset_index(inplace=True)
    cost_method_df = cost_df.drop(columns='total_daily_cost')
    cost_method_df['value_gas_sold'] = economics_df['value_gas_sold'] * -1

    # Average costs into per method per site per year.
    # Get adjusted program cost (costs - value gas sold).
    def cost_site_year(x):
        return (((x / n_sites) / timesteps) * 365)

    for column in cost_method_df.columns:
        if column != 'program_name':
            cost_method_df[column] = cost_method_df[column].map(cost_site_year)

    cost_method_df['adjusted_program_cost'] = cost_method_df.sum(axis=1)

    # Reconfigure df columns to have verification cost first.
    # Allows it to be at the bottom of the bar plot.
    second_column = cost_method_df.pop('verification_cost')
    cost_method_df.insert(1, 'verification_cost', second_column)
    cost_method_site_year_thousand = cost_method_df.set_index(
        'program_name') / 1000
    # converting to thousands for plotting

    # Plot up the cost/method/site/year cost for each program.
    cost_method_site_year_thousand.loc[
        :, 'verification_cost':'value_gas_sold'].plot.bar(stacked=True)
    plt.scatter(
        programs, cost_method_site_year_thousand['adjusted_program_cost'],
        marker='o',
        color='black', zorder=2,
        label='costs - gas sold')
    plt.xticks(rotation=0)
    plt.axhline(y=0, color="black", linestyle='solid')
    plt.ylabel("Cost/Benefit (Thousand $/site/year)")
    plt.xlabel("Program")
    plt.title("Costs and Benefits of LDAR Programs")
    plt.legend()
    plt.savefig(output_directory / 'cost_method_plot.png')

    # Output dataframes into csv's.
    economics_df.to_csv(output_directory / 'economics_outputs.csv', index=True)

    cost_method_site_year_thousand.to_csv(
        output_directory / 'annual_cost_method_site.csv', index=True)

    return economics_df
