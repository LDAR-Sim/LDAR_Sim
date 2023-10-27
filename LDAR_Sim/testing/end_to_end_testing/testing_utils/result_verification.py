import filecmp
import json
import logging
import math
import numbers

# import pickle
import subprocess
from datetime import datetime
from typing import Any, Literal

import yaml
from testing_utils.comparison_funcs import check_relative_similarity

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


def compare_params(out_dir, expected_dir) -> Literal["Success", "Failure"]:
    # Read in parameters and expected parameters
    with open(out_dir / "parameters.yaml", "r") as params_file:
        params: Any = yaml.safe_load(params_file)
    with open(expected_dir / "parameters.yaml", "r") as expected_params_file:
        expected_params: Any = yaml.safe_load((expected_params_file))
    # Check that parameters match as expected
    if params == expected_params:
        return "Success"
    return "Failure"


def compare_prog_tables(out_dir, expected_dir, logger) -> Literal["Success", "Failure"]:
    ret_string = "Success"

    # Read in program table and expected program table
    with open(out_dir / "prog_table.json", "r") as prog_table_file:
        prog_table_json: str = prog_table_file.read()
        prog_table: Any = json.loads(prog_table_json)
    with open(expected_dir / "prog_table.json", "r") as expected_prog_table_file:
        expected_prog_table_json: str = expected_prog_table_file.read()
        expected_prog_table: Any = json.loads(expected_prog_table_json)

    for prog, prog_e in zip(prog_table, expected_prog_table):
        # Iterate through results in the program table and compare them to the expected results.
        # If they are numeric, test that they are within 1% of each other,
        # otherwise they should match.
        for (metric, val), (e_metric, e_val) in zip(prog.items(), prog_e.items()):
            if metric != "program_name" and metric != "methods":
                if isinstance(e_val, numbers.Number) and not math.isnan(e_val):
                    stat_similar = check_relative_similarity(0.01, val, e_val)
                elif val == e_val or (math.isnan(val)) and math.isnan(e_val):
                    stat_similar = "Success"
                else:
                    stat_similar = "Failure"
                # Log the results of the comparison
                logger.info(
                    f"Program table Program: {prog['program_name']} comparison of {metric}"
                    + f" to expected value results in: {stat_similar}"
                )
                if stat_similar == "Failure":
                    ret_string = stat_similar
            elif metric == "methods":
                # Iterate through results relating to a method in the program table,
                # and compare them to the expected results.
                # If they are numeric, test that they are within 1% of each other,
                # otherwise they should match.
                for (method, m_vals), (e_method, e_m_vals) in zip(val.items(), e_val.items()):
                    for m_val, e_m_val in zip(m_vals, e_m_vals):
                        if isinstance(e_m_vals[e_m_val], numbers.Number) and not math.isnan(
                            e_m_vals[e_m_val]
                        ):
                            stat_similar: Literal["Success", "Failure"] = check_relative_similarity(
                                0.01, m_vals[m_val], e_m_vals[e_m_val]
                            )
                        elif (
                            m_vals[m_val] == e_m_vals[e_m_val]
                            or (math.isnan(m_vals[m_val]))
                            and math.isnan(e_m_vals[e_m_val])
                        ):
                            stat_similar = "Success"
                        else:
                            stat_similar = "Failure"
                        # Log the results of the comparison
                        logger.info(
                            f"Program table Program: {prog['program_name']}, method: {method}, "
                            f"comparison of {m_val} to expected "
                            f"value results in: {stat_similar}"
                        )
                    if stat_similar == "Failure":
                        ret_string = stat_similar
    return ret_string


def compare_out_files(out_dir, expected_results, logger) -> Literal["Success", "Failure"]:
    ret_string: Literal = "Success"

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

    # Check Program table is within acceptable range
    prog_table_match: Literal["Success", "Failure"] = compare_prog_tables(
        out_dir, expected_results, logger
    )
    logger.info(f"{'Programs comparison status:'} {prog_table_match}")

    # Compare filenames in expected outputs to outputs
    out_files_match: Literal["Success", "Failure"] = compare_out_files(
        out_dir, expected_results, logger
    )
    logger.info(f"{'Output Files comparison status:'} {out_files_match}")

    # Log Test Ending Message
    logger.info("End to End Testing Complete -----------------------------------------------------")

    # Close Handler and remove it from the logger
    file_handler.close()
    logger.removeHandler(file_handler)
    return None
