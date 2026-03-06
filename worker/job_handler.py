"""Orchestrate the full lifecycle of a single LDAR-Sim job.

Flow:
1. Parse SQS message → { runId, configId, orgId, config }
2. PATCH NestJS run status → running
3. Download S3 input files to temp dir
4. Write YAML config files to temp dir
5. Invoke ldar_sim_main.py as a subprocess
6. Parse CSV outputs
7. POST results to NestJS
8. NestJS marks run completed (via POST /results) — or mark failed on error
9. Clean up temp dir
"""
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from config_generator import generate_yaml_files
from result_parser import parse_all_results
from s3_client import download_input_files
from api_client import post_results, patch_run_status

logger = logging.getLogger(__name__)

# Absolute path to the LDAR-Sim Python package root (contains src/)
# worker/ is a sibling of LDAR_Sim/, so go up one level.
_LDAR_SIM_ROOT = Path(__file__).resolve().parent.parent / "LDAR_Sim"
_LDAR_SIM_MAIN = _LDAR_SIM_ROOT / "src" / "ldar_sim_main.py"

_S3_BUCKET = os.environ.get("LDAR_SIM_S3_BUCKET", "")


def handle_job(message_body: dict) -> None:
    """Process a single job message end-to-end."""
    run_id = message_body["runId"]
    config = message_body["config"]
    vw = config.get("virtual_world", {})

    logger.info("Starting job for run %d", run_id)

    temp_dir = tempfile.mkdtemp(prefix=f"ldar_sim_run_{run_id}_")
    params_dir = os.path.join(temp_dir, "params")
    input_dir = os.path.join(temp_dir, "inputs")
    output_dir = os.path.join(temp_dir, "outputs")
    os.makedirs(params_dir, exist_ok=True)
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    try:
        # ── Step 2: mark running ─────────────────────────────────────────────────
        patch_run_status(run_id, "running")

        # ── Step 3: download input files from S3 ────────────────────────────────
        infrastructure_key = vw.get("infrastructure_file", "")
        weather_key = vw.get("weather_file", "")

        if _S3_BUCKET and infrastructure_key and weather_key:
            file_map = download_input_files(
                bucket=_S3_BUCKET,
                infrastructure_key=infrastructure_key,
                weather_key=weather_key,
                dest_dir=input_dir,
            )
            infrastructure_filename = os.path.basename(
                file_map["infrastructure_file"]
            )
            weather_filename = os.path.basename(file_map["weather_file"])
        else:
            logger.warning(
                "S3 not configured or file keys missing — using filenames as-is: %s, %s",
                infrastructure_key,
                weather_key,
            )
            infrastructure_filename = os.path.basename(infrastructure_key) or "facilities.csv"
            weather_filename = os.path.basename(weather_key) or "weather.nc"

        # ── Step 4: write YAML config files ────────────────────────────────────
        generate_yaml_files(
            config=config,
            params_dir=params_dir,
            input_dir=input_dir,
            output_dir=output_dir,
            infrastructure_file=infrastructure_filename,
            weather_file=weather_filename,
        )

        # ── Step 5: invoke ldar_sim_main.py ────────────────────────────────────
        cmd = [
            sys.executable,
            str(_LDAR_SIM_MAIN),
            "--in_dir",
            params_dir,
            "--out_dir",
            output_dir,
        ]
        logger.info("Running simulation: %s", " ".join(cmd))
        result = subprocess.run(
            cmd,
            cwd=str(_LDAR_SIM_ROOT),
            capture_output=True,
            text=True,
            timeout=7200,  # 2-hour hard limit
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"ldar_sim_main.py exited with code {result.returncode}:\n"
                f"stdout: {result.stdout[-2000:]}\n"
                f"stderr: {result.stderr[-2000:]}"
            )

        logger.info("Simulation completed for run %d", run_id)

        # ── Step 6: parse CSV outputs ───────────────────────────────────────────
        parsed = parse_all_results(output_dir)

        # ── Step 7: POST results → NestJS (which marks completed internally) ───
        post_results(run_id, parsed)

        logger.info("Job for run %d finished successfully", run_id)

    except Exception as exc:
        logger.error("Job for run %d FAILED: %s", run_id, exc, exc_info=True)
        try:
            patch_run_status(run_id, "failed", error_message=str(exc)[:1000])
        except Exception:
            logger.error(
                "Could not mark run %d as failed — giving up", run_id, exc_info=True
            )
        raise

    finally:
        # ── Step 9: clean up temp directory ────────────────────────────────────
        try:
            shutil.rmtree(temp_dir)
            logger.info("Cleaned up temp dir %s", temp_dir)
        except Exception:
            logger.warning("Failed to clean up temp dir %s", temp_dir, exc_info=True)
