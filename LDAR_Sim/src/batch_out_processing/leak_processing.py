"""
Try to get 
Average leak duration
Average emission volume (kg)
Average rate
Max rate
Max volume
Min rate
Min volume
"""

import pandas as pd
import csv
import os


def leak_process(leaks):
    # Calculate the required statistics
    mean_values = leaks[['volume', 'rate', 'days_active']].mean()
    max_values = leaks[['volume', 'rate']].max()
    min_values = leaks[['volume', 'rate']].min()

    # Create or append to 'leak_summary.csv'
    with open('leak_summary.csv', 'a', newline='') as csvfile:
        fieldnames = ['volume_mean', 'volume_max', 'volume_min',
                      'rate_mean', 'rate_max', 'rate_min', 'days_active_mean']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # If the file doesn't exist, write the header
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write the calculated statistics
        writer.writerow({'volume_mean': mean_values['volume'],
                        'volume_max': max_values['volume'],
                         'volume_min': min_values['volume'],
                         'rate_mean': mean_values['rate'],
                         'rate_max': max_values['rate'],
                         'rate_min': min_values['rate'],
                         'days_active_mean': mean_values['days_active']})
