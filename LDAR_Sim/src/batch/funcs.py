import pandas as pd


def all_sites_used(in_dir, virtual_world):
    all_sites = True

    sites_file = virtual_world['infrastructure_file']
    sites_in = pd.read_csv(in_dir / sites_file)
    if virtual_world['site_samples'] != sites_in.shape[0]:
        all_sites = False
    return all_sites
