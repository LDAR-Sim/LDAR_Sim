import numpy as np
import csv
SITE_EMISSIONS = "total_emissions_kg"
SITE_LEAKS = "cum_leaks"

BATCH_SIMULATIONS = "batch_sims"
SITES_SUMMARY_FP = "sites_summary.csv"

LEAKS_SUMMARY_FP = "leaks_summary.csv"
LEAKS_RATE = "rate"
LEAKS_VOLUME = "volume"
LEAKS_DAYS_ACTIVE = "days_active"
TS_SUMMARY_FP = "timeseries_summary.csv"

TS_EMISSIONS = 'daily_emissions_kg'
TS_COST = 'total_daily_cost'
TS_REPAIR_COST = 'repair_cost'
TS_ACTIVE_LEAKS = 'active_leaks'
TS_NEW_LEAKS = 'new_leaks'
TS_N_TAGS = 'n_tags'

TS_SITE_VISITS = "sites_visited"
TS_EFFECTIVE_FLAGS = "eff_flags"


def write_sites_summary(site_df, summary_path, prog_name):
    site_summary = get_sites_summary(site_df, prog_name)

    with open(summary_path / SITES_SUMMARY_FP, mode='a', newline='') as sites_sum_file:
        fieldnames = site_summary.keys()
        writer = csv.DictWriter(sites_sum_file, fieldnames=fieldnames)

        if sites_sum_file.tell() == 0:
            writer.writeheader()

        writer.writerow(site_summary)


def get_sites_summary(site_df, prog_name):
    site_summary = {}
    site_summary.update([("Program", prog_name)])
    site_summary.update([("Mean_Emissions_per_site", site_df[SITE_EMISSIONS].mean())])
    site_summary.update([("5th_percentile_Emissions_per_site",
                        np.percentile(site_df[SITE_EMISSIONS], 5))])
    site_summary.update([("95th_percentile_Emissions_per_site",
                        np.percentile(site_df[SITE_EMISSIONS], 95))])
    site_summary.update([("Mean_leaks_per_site", site_df[SITE_LEAKS].mean())])
    site_summary.update([("5th_percentile_leaks_per_site", np.percentile(site_df[SITE_LEAKS], 5))])
    site_summary.update(
        [("95th_percentile_leaks_per_site", np.percentile(site_df[SITE_LEAKS], 95))])
    return site_summary


def write_leaks_summary(leaks_df, summary_path, prog_name):
    leaks_summary = get_leaks_summary(leaks_df, prog_name)

    with open(summary_path / LEAKS_SUMMARY_FP, mode='a', newline='') as leaks_sum_file:
        fieldnames = leaks_summary.keys()
        writer = csv.DictWriter(leaks_sum_file, fieldnames=fieldnames)

        if leaks_sum_file.tell() == 0:
            writer.writeheader()

        writer.writerow(leaks_summary)


def get_leaks_summary(leak_df, prog_name):
    leaks_summary = {}
    leaks_summary.update([("Program", prog_name)])
    leaks_summary.update([("Volume_mean", leak_df[LEAKS_VOLUME].mean())])
    leaks_summary.update([("5th_percentile_Volume",
                           np.percentile(leak_df[LEAKS_VOLUME], 5))])
    leaks_summary.update([("95th_percentile_Volume",
                           np.percentile(leak_df[LEAKS_VOLUME], 95))])
    leaks_summary.update([("Mean_leak_rate", leak_df[LEAKS_RATE].mean())])
    leaks_summary.update([("5th_percentile_Rate",
                           np.percentile(leak_df[LEAKS_RATE], 5))])
    leaks_summary.update([("95th_percentile_Rate",
                           np.percentile(leak_df[LEAKS_RATE], 95))])
    leaks_summary.update([("Mean_Days_Active", leak_df[LEAKS_DAYS_ACTIVE].mean())])
    leaks_summary.update([("5th_percentile_Days_Active",
                           np.percentile(leak_df[LEAKS_DAYS_ACTIVE], 5))])
    leaks_summary.update([("95th_percentile_Days_Active",
                           np.percentile(leak_df[LEAKS_DAYS_ACTIVE], 95))])

    return leaks_summary


def get_ts_summary(ts_df, prog_name):
    ts_summary = {}
    ts_summary_cols = [TS_EMISSIONS, TS_COST, TS_REPAIR_COST,
                       TS_ACTIVE_LEAKS, TS_NEW_LEAKS, TS_N_TAGS]
    ts_partial_cols_to_sum = [TS_SITE_VISITS, TS_EFFECTIVE_FLAGS, TS_N_TAGS]
    ts_summary.update([("Program", prog_name)])
    ts_summary.update([("Total Emissions", ts_df[TS_EMISSIONS].sum())])
    for col in ts_summary_cols:
        ts_summary.update([(f"Mean_{col}_per_day", ts_df[col].mean())])
        ts_summary.update([(f"5th_percentile_{col}_per_day", np.percentile(ts_df[col], 5))])
        ts_summary.update([(f"95th_percentile_{col}_per_day", np.percentile(ts_df[col], 95))])

    extra_stats = {}
    for df_col in ts_df.columns:
        for col in ts_partial_cols_to_sum:
            if col in df_col:
                extra_stats.update([(f"Sum_{df_col}_overall", ts_df[df_col].sum())])
    ts_summary.update([("Additional Statistics", extra_stats)])
    return ts_summary


def write_ts_summary(ts_df, summary_path, prog_name):
    site_summary = get_ts_summary(ts_df, prog_name)

    with open(summary_path / TS_SUMMARY_FP, mode='a', newline='') as ts_sum_file:
        fieldnames = site_summary.keys()
        writer = csv.DictWriter(ts_sum_file, fieldnames=fieldnames)

        if ts_sum_file.tell() == 0:
            writer.writeheader()

        writer.writerow(site_summary)
