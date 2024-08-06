"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        result_verification.py
Purpose: Contains functions for verifying E2E testing

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

import filecmp
import logging
import os

import subprocess
from datetime import datetime
from typing import Literal
import pandas as pd


DEFAULT_TEST_DIR: str = "testing/end_to_end_testing/test_results/"


def get_git_commit_hash() -> str | None:
    try:
        # run git command to get current commit hash
        git_commit_hash: str = (
            subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
        )
    except subprocess.CalledProcessError:
        # handle error if Git command fails
        git_commit_hash = None
    return git_commit_hash


def read_and_normalize_csv(file_path):
    """Read and normalize a CSV file by sorting and resetting index."""
    df = pd.read_csv(file_path)
    df_sorted = df.sort_values(by=list(df.columns)).reset_index(drop=True)
    return df_sorted


def compare_csvs(out_dir, expected_dir, logger) -> Literal["Success", "Failure"]:
    """Compare CSV files in out_dir with identically named CSV files in expected_dir."""
    # Get list of CSV files in out_dir
    out_csv_files = [f for f in os.listdir(out_dir) if f.endswith(".csv")]

    success = True

    for out_file in out_csv_files:
        out_file_path = os.path.join(out_dir, out_file)
        expected_file_path = os.path.join(expected_dir, out_file)

        if not os.path.exists(expected_file_path):
            logger.error(f"Expected file {expected_file_path} does not exist.")
            success = False
            continue

        try:
            out_df = read_and_normalize_csv(out_file_path)
            expected_df = read_and_normalize_csv(expected_file_path)

            if out_df.equals(expected_df):
                logger.info(f"Comparison of {out_file}: Success")
            else:
                logger.error(f"Comparison of {out_file}: Failure")
                success = False
        except Exception as e:
            logger.error(f"Error comparing {out_file}: {e}")
            success = False

    return "Success" if success else "Failure"


def compare_out_files(out_dir, expected_results, logger) -> Literal["Success", "Failure"]:
    ret_string: Literal["Success", "Failure"] = "Success"

    # Setup Directory Comparison
    comparison: filecmp.dircmp = filecmp.dircmp(out_dir, expected_results)
    non_identical_files_batch: list = []

    # Compare files in top-level output directories
    if comparison.left_only or comparison.right_only:
        ret_string = "Failure"  # Directories have differences
        non_identical_files_batch.extend(comparison.left_only + comparison.right_only)
        non_identical_files_print: str = ", ".join(
            [str(element) for element in non_identical_files_batch]
        )
        logger.info(f"Non-Identical files found in batch outputs: {non_identical_files_print}")
    else:
        logger.info("Batch outputs identical")

    # Loop through each program directory and compare
    for subdir in comparison.common_dirs:
        non_identical_files_program: list = []
        sub_comp: filecmp.dircmp = filecmp.dircmp(
            f"{out_dir}/{subdir}", f"{expected_results}/{subdir}"
        )
        if sub_comp.left_only or sub_comp.right_only:
            ret_string = "Failure"
            non_identical_files_program.extend(sub_comp.left_only + sub_comp.right_only)
            non_identical_files_print: str = ", ".join(
                [str(element) for element in non_identical_files_program]
            )
            logger.info(
                f"Non-Identical files found in Program {subdir} "
                f"directory: {non_identical_files_print}"
            )
        else:
            logger.info(f"All files in Program {subdir} directory identical")

    return ret_string


def compare_outputs(
    test_case, out_dir, expected_results, test_results_dir=DEFAULT_TEST_DIR
) -> None:
    # Setup logging
    git_hash: str | None = get_git_commit_hash()
    logger: logging.Logger = logging.getLogger("E2E Testing Results")
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(f"{test_results_dir}{test_case}_{git_hash}.log")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter()
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Log timestamp
    cur_time: datetime = datetime.now()
    logger.info(f"E2E test initialization time: {cur_time}")

    # Check Parameter match expected - CURRENTLY DISABLED
    # params_match: Literal['Success', 'Failure'] = compare_params(out_dir, expected_results)
    # logger.info(f"{'Parameters comparison status:'} {params_match}")

    # Compare filenames in expected outputs to outputs
    out_files_match: Literal["Success", "Failure"] = compare_out_files(
        out_dir, expected_results, logger
    )
    logger.info(f"{'Output Files comparison status:'} {out_files_match}")

    # Check Summary CSVs are within acceptable range
    csv_match: Literal["Success", "Failure"] = compare_csvs(out_dir, expected_results, logger)
    logger.info(f"{'Summary comparison status:'} {csv_match}")

    # Log Test Ending Message
    logger.info("End to End Testing Complete -----------------------------------------------------")

    # Close Handler and remove it from the logger
    file_handler.close()
    logger.removeHandler(file_handler)
    return None
