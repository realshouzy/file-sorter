#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Module responsible for handling the JSON configs."""
from __future__ import annotations

__all__: list[str] = ["read_from_configs", "write_to_configs"]

import json
import logging

from auto_file_sorter.constants import CONFIG_LOG_LEVEL, CONFIGS_LOCATION, EXIT_FAILURE


def read_from_configs() -> dict[str, str]:
    """Function wrapping ``open`` for reading from ``configs.json``."""
    reading_logger: logging.Logger = logging.getLogger(read_from_configs.__name__)
    try:
        reading_logger.debug("Opening %s", CONFIGS_LOCATION)
        with open(CONFIGS_LOCATION, "r", encoding="utf-8") as json_file:
            reading_logger.debug("Loading %s", json_file)
            configs_dict: dict[str, str] = json.load(json_file)
    except FileNotFoundError as no_file_err:
        reading_logger.critical(
            "Unable to find 'configs.json', falling back to an empty configuration",
        )
        configs_dict = {}
        write_to_configs(configs_dict)
        raise SystemExit(EXIT_FAILURE) from no_file_err
    except PermissionError as perm_err:
        reading_logger.critical(
            "Permission denied to open and read from '%s'",
            CONFIGS_LOCATION,
        )
        raise SystemExit(EXIT_FAILURE) from perm_err
    except OSError as os_err:
        reading_logger.critical(
            "I/O-related error occurred while opening and reading from '%s'",
            CONFIGS_LOCATION,
        )
        raise SystemExit(EXIT_FAILURE) from os_err
    except json.JSONDecodeError as json_decode_err:
        reading_logger.critical(
            "Given JSON file is not correctly formatted: %s",
            CONFIGS_LOCATION,
        )
        raise SystemExit(EXIT_FAILURE) from json_decode_err
    except Exception as err:
        reading_logger.exception("Unexpected %s", err.__class__.__name__)
        raise SystemExit(EXIT_FAILURE) from err
    reading_logger.log(
        CONFIG_LOG_LEVEL,
        "Read from %s",
        CONFIGS_LOCATION,
    )
    return configs_dict


def write_to_configs(new_configs: dict[str, str]) -> None:
    """Function wrapping ``open`` for writing to ``configs.json``."""
    writing_logger: logging.Logger = logging.getLogger(write_to_configs.__name__)
    try:
        writing_logger.debug("Opening '%s'", CONFIGS_LOCATION)
        with open(CONFIGS_LOCATION, "w", encoding="utf-8") as json_file:
            writing_logger.debug("Dumping: %s", new_configs)
            json.dump(new_configs, json_file, indent=4)
    except TypeError as type_err:
        writing_logger.critical(
            "Given JSON file is not correctly configured: %s",
            CONFIGS_LOCATION,
        )
        raise SystemExit(EXIT_FAILURE) from type_err
    except PermissionError as perm_err:
        writing_logger.critical(
            "Permission denied to open and read from '%s'",
            CONFIGS_LOCATION,
        )
        raise SystemExit(EXIT_FAILURE) from perm_err
    except FileNotFoundError as no_file_err:
        writing_logger.critical(
            "Unable to find '%s'",
            CONFIGS_LOCATION,
        )
        raise SystemExit(EXIT_FAILURE) from no_file_err
    except OSError as os_err:
        writing_logger.critical(
            "I/O-related error occurred while opening and reading from '%s'",
            CONFIGS_LOCATION,
        )
        raise SystemExit(EXIT_FAILURE) from os_err
    except Exception as err:
        writing_logger.exception("Unexpected %s", err.__class__.__name__)
        raise SystemExit(EXIT_FAILURE) from err
    writing_logger.log(
        CONFIG_LOG_LEVEL,
        "Added new extension configuration: %s",
        new_configs,
    )
