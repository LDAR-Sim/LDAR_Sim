"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        logging_config.py
Purpose:    Contains functions to configure logging for LDAR-Sim.

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

import logging
import os
import sys
from pathlib import Path

from constants.file_processing_const import IOLocationConstants as io_loc


def setup_error_logging(
    log_folder: Path,
    timestamp: str,
    log_to_file: bool = True,
    log_to_console: bool = True,
) -> None:
    # Get the root logger
    logger: logging.Logger = logging.getLogger()

    # If log to file is enabled, create a file handler and add it to the logger
    if log_to_file:
        error_file_handler: logging.FileHandler = logging.FileHandler(
            log_folder / f"{timestamp}_error.log"
        )
        error_file_handler.setLevel(logging.ERROR)
        error_file_logging_format: logging.Formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
        )
        error_file_handler.setFormatter(error_file_logging_format)
        logger.addHandler(error_file_handler)

    # If log to console is enabled, create a stream handler and add it to the logger
    if log_to_console:
        error_stream_handler: logging.StreamHandler = logging.StreamHandler(sys.stderr)
        error_stream_handler.setLevel(logging.ERROR)
        error_stream_logging_format: logging.Formatter = logging.Formatter(
            "%(levelname)s: %(message)s"
        )
        error_stream_handler.setFormatter(error_stream_logging_format)
        logger.addHandler(error_stream_handler)


def setup_logging_to_output(output_folder: Path) -> None:
    # Get the root logger
    logger: logging.Logger = logging.getLogger()

    # Check if log folder exists, if not create it
    log_folder: Path = output_folder / io_loc.LOG_FOLDER

    if not log_folder.exists():
        os.mkdir(log_folder)

    # Add a new file handler to the logger
    output_error_file_handler: logging.FileHandler = logging.FileHandler(log_folder / "error.log")
    output_error_file_handler.setLevel(logging.ERROR)
    error_file_logging_format: logging.Formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
    )
    output_error_file_handler.setFormatter(error_file_logging_format)
    logger.addHandler(output_error_file_handler)
