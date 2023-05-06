import logging
import subprocess

DEFAULT_TEST_DIR: str = "testing/end_to_end_testing/test_results/"


def get_git_commit_hash() -> str | None:
    try:
        # run git command to get current commit hash
        git_commit_hash: str = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        # handle error if Git command fails
        git_commit_hash = None
    return git_commit_hash


def compare_params(out_dir, logger):
    return "Failure"


def compare_outputs(test_case, out_prog_table, out_dir, sim_outputs,
                    expected_results, test_results_dir=DEFAULT_TEST_DIR) -> None:
    # Setup logging
    git_hash: str | None = get_git_commit_hash()
    logger: logging.Logger = logging.getLogger("E2E Testing Results")
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(
        f"{test_results_dir}{test_case}_{git_hash}.log")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter()
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Check Parameter match expected
    params_match = compare_params(out_dir, logger)
    logger.info(f"Parameters comparison status: {params_match}")

    # Close Handler and remove it from the logger
    file_handler.close()
    logger.removeHandler(file_handler)
    return None
