import pandas as pd

SUBTYPE_CODE = "subtype_code"
LAT = "lat"
LON = "lon"
EQUIP_GROUPS = "equipment_groups"
ID = "facility_ID"

CUM_LEAKS = "cum_leaks"
INITIAL_LEAKS = "initial_leaks"
EMISSIONS = "total_emissions_kg"

SIM_COUNT = "n_sims"

COLS_TO_CONCAT = [CUM_LEAKS, INITIAL_LEAKS, EMISSIONS]
COLS_TO_KEEP = [SUBTYPE_CODE, LAT, LON, EQUIP_GROUPS, ID]


def concat_sites(site_df1, site_df2):
    combined_cols = COLS_TO_CONCAT + COLS_TO_KEEP
    combined_df = pd.DataFrame(columns=combined_cols)
    sorted_site_df1 = site_df1.sort_values(by=ID)
    sorted_site_df2 = site_df2.sort_values(by=ID)

    # Copy over columns that should be constant in between sims for sites
    for col in COLS_TO_KEEP:
        combined_df[col] = sorted_site_df1[col]

    # Set ID as the index so we can sum by ID
    sorted_site_df1.set_index(ID, inplace=True)
    sorted_site_df2.set_index(ID, inplace=True)
    combined_df.set_index(ID, inplace=True)

    # Calculate mean for output statistic columns
    for col in COLS_TO_CONCAT:
        n_sims_df1 = sorted_site_df1[SIM_COUNT][0] if SIM_COUNT in sorted_site_df1.columns else 1
        n_sims_df2 = sorted_site_df2[SIM_COUNT][0] if SIM_COUNT in sorted_site_df2.columns else 1
        combined_df[col] = ((sorted_site_df1[col] * n_sims_df1) +
                            (sorted_site_df2[col] * n_sims_df2))/(n_sims_df1 + n_sims_df2)
    # Update the simulation count so future concatenations can do the mean properly
    combined_df[SIM_COUNT] = (n_sims_df1 + n_sims_df2)

    # Reset the combined df index so we get ID's in the csv
    combined_df.reset_index(inplace=True)
    return combined_df


def make_sites_output(sites_df):
    # Define columns to concatenate and columns to keep
    combined_cols = COLS_TO_CONCAT + COLS_TO_KEEP

    # Create an empty DataFrame with the desired columns
    combined_df = pd.DataFrame(columns=combined_cols)

    # Sort the input DataFrame by ID
    sorted_site_df1 = sites_df.sort_values(by=ID)

    # Copy over columns that should be constant between simulations for sites
    for col in COLS_TO_KEEP:
        combined_df[col] = sorted_site_df1[col]

    # Set ID as the index for both DataFrames
    sorted_site_df1.set_index(ID, inplace=True)
    combined_df.set_index(ID, inplace=True)

    # Copy over columns to concatenate, considering SIM_COUNT if present
    for col in COLS_TO_CONCAT:
        n_sims_df1 = sorted_site_df1['SIM_COUNT'].iloc[0] if 'SIM_COUNT' in sorted_site_df1.columns else 1
        combined_df[col] = sorted_site_df1[col]

    # Add the SIM_COUNT column to the combined DataFrame
    combined_df['SIM_COUNT'] = n_sims_df1

    # Reset the index of the combined DataFrame to include IDs in the CSV
    combined_df.reset_index(inplace=True)

    return combined_df


def concat_sites_files(sites_fp_1, sites_fp_2, combined_fp):
    sites_df1 = pd.read_csv(sites_fp_1)
    sites_df2 = pd.read_csv(sites_fp_2)
    combined_df = concat_sites(sites_df1, sites_df2)
    combined_df.to_csv(combined_fp, index=False)


def sites_files_output(sites_fp_1, output_fp):
    sites_df1 = pd.read_csv(sites_fp_1)
    output_df = make_sites_output(sites_df1)
    output_df.to_csv(output_fp, index=False)
