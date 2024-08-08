# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Generic functions
# Purpose:     Generic functions for running LDAR-Sim.
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------

import logging
import os
import sys
from pathlib import Path

import boto3
import numpy as np
from botocore.exceptions import ClientError
from constants.error_messages import Initialization_Messages as im
from constants.output_messages import RuntimeMessages as rm
import constants.param_default_const as pdc


def check_ERA5_file(dir, v_world):
    my_file = Path(dir / v_world[pdc.Virtual_World_Params.WEATHER_FILE])
    if my_file.is_file():
        print(rm.CHECK_WEATHER)
    else:
        print(rm.ATTEMPT_AWS_WEATHER_DOWNLOAD)
        try:
            access_key = os.getenv("AWS_KEY")
            secret_key = os.getenv("AWS_SEC")
        except Exception:
            print(im.AWS_KEY_SEC_ERROR)

        try:
            s3 = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
            s3.download_file(
                "im3sweather",
                v_world[pdc.Virtual_World_Params.WEATHER_FILE],
                r"{}/{}".format(dir, v_world[pdc.Virtual_World_Params.WEATHER_FILE]),
            )
        except ClientError:
            logger: logging.Logger = logging.getLogger(__name__)
            logger.error(im.ERA_AUTH_ERROR)
            sys.exit()
        print(rm.COMPLETE_WEATHER_DOWNLOAD)


def find_closest_index_numpy(arr, x):
    idx = np.searchsorted(arr, x)
    if idx == len(arr):
        return len(arr) - 1
    elif idx == 0:
        return 0
    else:
        before = abs(arr[idx - 1] - x)
        after = abs(arr[idx] - x)
        if before < after:
            return idx - 1
        else:
            return idx
