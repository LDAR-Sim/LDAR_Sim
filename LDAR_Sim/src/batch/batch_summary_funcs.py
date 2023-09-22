import numpy as np
import csv
SITE_EMISSIONS = "total_emissions_kg"
SITE_LEAKS = "cum_leaks"

BATCH_SIMULATIONS = "batch_sims"
SITES_SUMMARY_FP = "sites_summary.csv"


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
