"""Parse LDAR-Sim CSV outputs into structured dicts suitable for the NestJS API.

Output directory layout produced by ldar_sim_main.py:

    <out_dir>/
        <ProgramName>/
            timeseries_output_<n>_<ProgramName>.csv
            leaks_output_<n>_<ProgramName>.csv
            sites_output_<n>_<ProgramName>.csv
"""
import os
import re
import glob
import logging
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


# kg/hour → g/s conversion factor
_KGH_TO_GS = 1000.0 / 3600.0


def _safe_float(val) -> Optional[float]:
    try:
        f = float(val)
        return None if pd.isna(f) else f
    except (TypeError, ValueError):
        return None


def _safe_int(val) -> Optional[int]:
    f = _safe_float(val)
    return None if f is None else int(f)


def _safe_str(val) -> Optional[str]:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    return str(val) if str(val) not in ("nan", "None", "") else None


def parse_timeseries(csv_path: str, program_name: str, sim_index: int) -> list:
    """Parse a timeseries CSV and return a list of row dicts."""
    df = pd.read_csv(csv_path)
    rows = []
    for _, row in df.iterrows():
        rows.append(
            {
                "programName": program_name,
                "simIndex": sim_index,
                "date": _safe_str(row.get("datetime")),
                "activeLeaks": _safe_int(row.get("active_leaks")),
                "newLeaks": _safe_int(row.get("new_leaks")),
                "nTags": _safe_int(row.get("n_tags")),
                "dailyEmissionsKg": _safe_float(row.get("daily_emissions_kg")),
                "totalDailyCost": _safe_float(row.get("total_daily_cost")),
                "repairCost": _safe_float(row.get("repair_cost")),
                # Sum all <method>_cost columns as methodCost
                "methodCost": _safe_float(
                    sum(
                        row[c]
                        for c in df.columns
                        if c.endswith("_cost") and c != "repair_cost" and c != "verification_cost"
                        and not pd.isna(row[c])
                    )
                ),
            }
        )
    return rows


def parse_leaks(csv_path: str, program_name: str, sim_index: int) -> list:
    """Parse a leaks CSV and return a list of row dicts."""
    df = pd.read_csv(csv_path)
    rows = []
    for _, row in df.iterrows():
        # rate column is in kg/hour → convert to g/s
        rate_kgh = _safe_float(row.get("rate"))
        rate_gs = rate_kgh * _KGH_TO_GS if rate_kgh is not None else None

        # volume is in kg (cumulative)
        volume_kg = _safe_float(row.get("volume"))

        # Determine which method tagged the leak
        tagged_by = _safe_str(row.get("tagged_by_company"))

        rows.append(
            {
                "programName": program_name,
                "simIndex": sim_index,
                "leakId": _safe_str(row.get("leak_ID")),
                "facilityId": _safe_str(row.get("facility_ID")),
                "rateGs": rate_gs,
                "volumeKg": volume_kg,
                "status": _safe_str(row.get("status")),
                "daysActive": _safe_int(row.get("days_active")),
                "dateBegan": _safe_str(row.get("date_began")),
                "dateTagged": _safe_str(row.get("date_tagged")),
                "dateRepaired": _safe_str(row.get("date_repaired")),
                "taggedByMethod": tagged_by,
            }
        )
    return rows


def parse_sites(csv_path: str, program_name: str, sim_index: int) -> list:
    """Parse a sites CSV and return a list of row dicts."""
    df = pd.read_csv(csv_path)
    rows = []
    for _, row in df.iterrows():
        # Determine surveys_conducted: look for any <method>_surveys_conducted column
        surveys = None
        for col in df.columns:
            if col.endswith("_surveys_conducted"):
                surveys = _safe_int(row.get(col))
                if surveys is not None:
                    break

        rows.append(
            {
                "programName": program_name,
                "simIndex": sim_index,
                "facilityId": _safe_str(row.get("facility_ID")),
                "lat": _safe_float(row.get("lat")),
                "lon": _safe_float(row.get("lon")),
                "totalEmissionsKg": _safe_float(row.get("total_emissions_kg")),
                "activeLeakCount": _safe_int(row.get("active_leak_cnt")),
                "repairedLeakCount": _safe_int(row.get("repaired_leak_cnt")),
                "surveysConducted": surveys,
            }
        )
    return rows


def parse_all_results(out_dir: str) -> dict:
    """Walk the output directory and parse all CSV outputs.

    Returns:
        {
            "timeseries": [...],
            "leaks": [...],
            "sites": [...],
        }
    """
    timeseries_rows = []
    leaks_rows = []
    sites_rows = []

    # Each program has its own subdirectory
    for program_dir in sorted(os.listdir(out_dir)):
        full_program_dir = os.path.join(out_dir, program_dir)
        if not os.path.isdir(full_program_dir):
            continue

        # timeseries_output_<n>_<program>.csv
        for ts_path in glob.glob(
            os.path.join(full_program_dir, "timeseries_output_*.csv")
        ):
            match = re.search(r"timeseries_output_(\d+)_(.+)\.csv$", ts_path)
            if not match:
                continue
            sim_index = int(match.group(1))
            prog_name = match.group(2)
            logger.info("Parsing timeseries: %s", ts_path)
            timeseries_rows.extend(parse_timeseries(ts_path, prog_name, sim_index))

        # leaks_output_<n>_<program>.csv
        for leaks_path in glob.glob(
            os.path.join(full_program_dir, "leaks_output_*.csv")
        ):
            match = re.search(r"leaks_output_(\d+)_(.+)\.csv$", leaks_path)
            if not match:
                continue
            sim_index = int(match.group(1))
            prog_name = match.group(2)
            logger.info("Parsing leaks: %s", leaks_path)
            leaks_rows.extend(parse_leaks(leaks_path, prog_name, sim_index))

        # sites_output_<n>_<program>.csv
        for sites_path in glob.glob(
            os.path.join(full_program_dir, "sites_output_*.csv")
        ):
            match = re.search(r"sites_output_(\d+)_(.+)\.csv$", sites_path)
            if not match:
                continue
            sim_index = int(match.group(1))
            prog_name = match.group(2)
            logger.info("Parsing sites: %s", sites_path)
            sites_rows.extend(parse_sites(sites_path, prog_name, sim_index))

    return {
        "timeseries": timeseries_rows,
        "leaks": leaks_rows,
        "sites": sites_rows,
    }
