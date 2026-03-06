"""Convert a stored LDAR-Sim JSON config into the 4-file YAML layout expected
by ldar_sim_main.py:

    <params_dir>/
        simulation_settings.yaml
        virtual_world.yaml
        P_<name>.yaml          (one per program)
        M_<label>.yaml         (one per method)
"""
import os
import logging

import yaml

logger = logging.getLogger(__name__)

# LDAR-Sim parameter version written into every file
_VERSION = "3.0"


def _dump(obj: dict, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        yaml.dump(obj, fh, default_flow_style=False, sort_keys=False)
    logger.info("Wrote %s", path)


def generate_yaml_files(
    config: dict,
    params_dir: str,
    input_dir: str,
    output_dir: str,
    infrastructure_file: str,
    weather_file: str,
) -> None:
    """Write all YAML parameter files into *params_dir*.

    Args:
        config: The full 4-level config dict from the database (matches the
                LdarSimConfig TypeScript schema).
        params_dir: Directory where YAML files will be written.
        input_dir: Absolute path to the directory containing the downloaded
                   weather / infrastructure input files.
        output_dir: Absolute path for simulation outputs.
        infrastructure_file: Filename (not path) of the downloaded facilities CSV.
        weather_file: Filename (not path) of the downloaded weather NetCDF file.
    """
    sim = config.get("simulation_settings", {})
    vw = config.get("virtual_world", {})
    programs = config.get("programs", [])
    methods = config.get("methods", [])

    # ── simulation_settings.yaml ────────────────────────────────────────────────
    outputs = sim.get("outputs", {})
    sim_yaml = {
        "parameter_level": "simulation_settings",
        "version": _VERSION,
        "input_directory": input_dir,
        "output_directory": output_dir,
        "n_simulations": sim.get("n_simulations", 2),
        "n_processes": sim.get("n_processes", 1),
        "start_date": sim.get("start_date", [2017, 1, 1]),
        "end_date": sim.get("end_date", [2021, 12, 31]),
        "pregenerate_leaks": sim.get("pregenerate_leaks", False),
        "preseed_random": sim.get("preseed_random", False),
        # Pick first program as reference/baseline, or fall back to defaults
        "reference_program": programs[0]["program_name"] if programs else "P_none",
        "baseline_program": programs[-1]["program_name"] if len(programs) > 1 else (programs[0]["program_name"] if programs else "P_none"),
        "outputs": {
            "leaks": outputs.get("leaks", True),
            "sites": outputs.get("sites", True),
            "timeseries": outputs.get("timeseries", True),
            "plots": outputs.get("plots", False),
            "batch_reporting": outputs.get("batch_reporting", False),
        },
    }
    _dump(sim_yaml, os.path.join(params_dir, "simulation_settings.yaml"))

    # ── virtual_world.yaml ──────────────────────────────────────────────────────
    emissions = vw.get("emissions", {})
    repair_delay = vw.get("repair_delay", {"type": "default", "val": [0]})
    vw_yaml = {
        "parameter_level": "virtual_world",
        "version": _VERSION,
        "infrastructure_file": infrastructure_file,
        "weather_file": weather_file,
        "weather_is_hourly": vw.get("weather_is_hourly", True),
        "consider_weather": vw.get("consider_weather", True),
        "NRd": vw.get("NRd", 365),
        "n_init_leaks_prob": vw.get("n_init_leaks_prob", 0),
        "n_init_days": vw.get("n_init_days", 0),
        "repair_delay": repair_delay,
        "emissions": {
            "consider_venting": emissions.get("consider_venting", False),
            "LPR": emissions.get("LPR", 0.0065),
            "max_leak_rate": emissions.get("max_leak_rate", 100000),
            "leak_dist_params": emissions.get("leak_dist_params", [-1.79, 2.17]),
            "leak_dist_type": emissions.get("leak_dist_type", "lognorm"),
            "units": emissions.get("units", ["kilogram", "hour"]),
        },
    }
    if vw.get("site_samples") is not None:
        vw_yaml["site_samples"] = vw["site_samples"]
    _dump(vw_yaml, os.path.join(params_dir, "virtual_world.yaml"))

    # ── P_<name>.yaml — one per program ─────────────────────────────────────────
    for program in programs:
        name = program["program_name"]
        economics = program.get("economics", {})
        repair_costs = economics.get("repair_costs", {"vals": [0]})
        prog_yaml = {
            "parameter_level": "program",
            "version": _VERSION,
            "program_name": name,
            "method_labels": program.get("method_labels", []),
            "economics": {
                "carbon_price_tonnesCO2e": economics.get("carbon_price_tonnesCO2e", 0),
                "cost_CCUS": economics.get("cost_CCUS", 0),
                "GWP_CH4": economics.get("GWP_CH4", 25),
                "sale_price_natgas": economics.get("sale_price_natgas", 0),
                "repair_costs": {"vals": repair_costs.get("vals", [0])},
                "verification_cost": economics.get("verification_cost", 0),
            },
        }
        _dump(prog_yaml, os.path.join(params_dir, f"P_{name}.yaml"))

    # ── M_<label>.yaml — one per method ─────────────────────────────────────────
    for method in methods:
        label = method["label"]
        sensor = method.get("sensor", {})
        cost = method.get("cost", {})
        scheduling = method.get("scheduling", {})
        weather_envs = method.get("weather_envs", {})
        follow_up = method.get("follow_up", {})
        t_bw_sites = method.get("t_bw_sites", {"vals": [30]})

        meth_yaml = {
            "parameter_level": "method",
            "version": _VERSION,
            "label": label,
            "measurement_scale": method.get("measurement_scale", "component"),
            "deployment_type": method.get("deployment_type", "mobile"),
            "sensor": {
                "type": sensor.get("type", "default"),
                "MDL": sensor.get("MDL", [0.01]),
            },
            "cost": {
                "per_day": cost.get("per_day", 0),
                "per_hour": cost.get("per_hour", 0),
                "per_site": cost.get("per_site", 500),
                "upfront": cost.get("upfront", 0),
            },
            "n_crews": method.get("n_crews", 1),
            "consider_daylight": method.get("consider_daylight", False),
            "RS": method.get("RS", 4),
            "time": method.get("time", 120),
            "max_workday": method.get("max_workday", 10),
            "reporting_delay": method.get("reporting_delay", 0),
            "t_bw_sites": {"vals": t_bw_sites.get("vals", [30])},
            "scheduling": {
                "deployment_months": scheduling.get(
                    "deployment_months", list(range(1, 13))
                ),
                "deployment_years": scheduling.get("deployment_years", []),
                "LDAR_crew_init_location": scheduling.get(
                    "LDAR_crew_init_location", [0, 0]
                ),
                "route_planning": scheduling.get("route_planning", False),
                "min_time_bt_surveys": scheduling.get("min_time_bt_surveys", 0),
            },
            "weather_envs": {
                "precip": weather_envs.get("precip", [0, 10]),
                "temp": weather_envs.get("temp", [-40, 40]),
                "wind": weather_envs.get("wind", [0, 20]),
            },
            "is_follow_up": method.get("is_follow_up", False),
            "follow_up": {
                "preferred_method": follow_up.get("preferred_method", None),
                "delay": follow_up.get("delay", 0),
                "instant_threshold": follow_up.get("instant_threshold", 0),
                "instant_threshold_type": follow_up.get(
                    "instant_threshold_type", "absolute"
                ),
                "proportion": follow_up.get("proportion", 1),
                "threshold": follow_up.get("threshold", 0),
                "threshold_type": follow_up.get("threshold_type", "absolute"),
                "sort_by_rate": follow_up.get("sort_by_rate", False),
            },
        }
        if sensor.get("QE") is not None:
            meth_yaml["sensor"]["QE"] = sensor["QE"]

        _dump(meth_yaml, os.path.join(params_dir, f"M_{label}.yaml"))
