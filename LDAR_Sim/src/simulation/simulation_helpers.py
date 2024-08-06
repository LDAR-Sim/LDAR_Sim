import copy

from math import floor
from pathlib import Path


from ldar_sim import LdarSim
from programs.program import Program

from constants import param_default_const as pdc
from constants.output_messages import RuntimeMessages as rm
from virtual_world.infrastructure import Infrastructure


from datetime import date


import gc


def batch_simulations(simulation_count: int) -> list[int]:
    if simulation_count > 5:
        simulation_batches = floor(simulation_count / 5.0)
        sim_counts = [5] * simulation_batches
        remainder = simulation_count % 5
        if remainder > 0:
            sim_counts.append(remainder)
    else:
        sim_counts = [simulation_count]

    return sim_counts


def simulate(
    daylight,
    weather,
    sim_num: int,
    prog_name: str,
    meth_params,
    prog_param,
    sim_settings,
    virtual_world,
    output_params,
    infrastructure: Infrastructure,
    input_dir: Path,
    output_dir: Path,
    preseed_timeseries,
    lock,
    prog_measured_df,
):
    if lock is not None:
        with lock:
            infra = copy.deepcopy(infrastructure)
    else:
        infra = copy.deepcopy(infrastructure)
    gc.collect()
    program: Program = Program(
        prog_name,
        weather,
        daylight,
        meth_params,
        infra._sites,
        date(*virtual_world[pdc.Virtual_World_Params.START_DATE]),
        date(*virtual_world[pdc.Virtual_World_Params.END_DATE]),
        virtual_world[pdc.Virtual_World_Params.CONSIDER_WEATHER],
        prog_param,
        input_dir=input_dir,
    )
    infra.setup(program.get_method_names())
    print(rm.SIM_PROG.format(prog_name=prog_name))
    simulation: LdarSim = LdarSim(
        sim_num,
        sim_settings,
        virtual_world,
        output_params,
        program,
        infra,
        input_dir,
        output_dir,
        preseed_timeseries,
        prog_measured_df,
    )
    simulation.run_simulation()
    print(rm.FIN_PROG.format(prog_name=prog_name))
    gc.collect()
    return
