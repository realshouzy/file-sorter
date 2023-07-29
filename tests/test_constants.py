"""Module testing ``auto-file-sorter.constants.py``."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from auto_file_sorter.constants import (
    CONFIG_LOG_LEVEL,
    DEFAULT_CONFIGS_LOCATION,
    DEFAULT_LOG_LOCATION,
    EXIT_FAILURE,
    EXIT_SUCCESS,
    FILE_EXTENSION_PATTERN,
    LOG_FORMAT,
    MAX_VERBOSITY_LEVEL,
    MOVE_LOG_LEVEL,
    PROGRAM_LOCATION,
    STREAM_HANDLER_FORMATTER,
)

if TYPE_CHECKING:
    from collections.abc import Callable

# pylint: disable=C0116, W0212


@pytest.mark.parametrize(
    ("constant", "expected_value"),
    (
        pytest.param(CONFIG_LOG_LEVEL, 70, id="CONFIG_LOG_LEVEL"),
        pytest.param(MOVE_LOG_LEVEL, 60, id="MOVE_LOG_LEVEL"),
        pytest.param(
            LOG_FORMAT,
            "%(name)s [%(levelname)s] %(asctime)s - %(message)s",
            id="LOG_FORMAT-%(name)s [%(levelname)s] %(asctime)s - %(message)s",
        ),
        pytest.param(MAX_VERBOSITY_LEVEL, 3, id="MAX_VERBOSITY_LEVEL"),
        pytest.param(EXIT_SUCCESS, 0, id="EXIT_SUCCESS"),
        pytest.param(EXIT_FAILURE, 1, id="EXIT_FAILURE"),
        pytest.param(
            STREAM_HANDLER_FORMATTER._fmt,
            "[%(levelname)s] %(message)s",
            id="STREAM_HANDLER_FORMATTER-[%(levelname)s] %(message)s",
        ),
    ),
)
def test_constants(constant: int | str, expected_value: int | str) -> None:
    assert constant == expected_value


@pytest.mark.parametrize(
    "location_check",
    (
        pytest.param(PROGRAM_LOCATION.is_dir, id="PROGRAM_LOCATION-is_dir"),
        pytest.param(DEFAULT_CONFIGS_LOCATION.is_file, id="CONFIGS_LOCATIO-is_file"),
        pytest.param(DEFAULT_LOG_LOCATION.is_file, id="DEFAULT_LOG_LOCATION-is_file"),
    ),
)
def test_locations(location_check: Callable[[], bool]) -> None:
    assert location_check()


@pytest.mark.parametrize(
    "extension",
    (
        pytest.param(".TXT"),
        pytest.param(".zip"),
        pytest.param(".7z"),
        pytest.param(".123"),
        pytest.param(".PnG"),
        pytest.param(".Jp2"),
    ),
)
def test_file_valid_extension_pattern(extension: str) -> None:
    assert FILE_EXTENSION_PATTERN.fullmatch(extension) is not None


@pytest.mark.parametrize(
    "extension",
    (
        pytest.param("TXT"),
        pytest.param("zip"),
        pytest.param("_7z_"),
        pytest.param("-123"),
        pytest.param(".PnG!"),
        pytest.param(".Jp2@"),
        pytest.param("/doc"),
        pytest.param(""),
    ),
)
def test_file_invalid_extension_pattern(extension: str) -> None:
    assert FILE_EXTENSION_PATTERN.fullmatch(extension) is None
