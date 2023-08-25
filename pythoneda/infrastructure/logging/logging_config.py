"""
pythoneda/infrastructure/logging/logging_config.py

This file configures PythonEDA logging.

Copyright (C) 2023-today rydnr's pythoneda-shared-pythoneda/infrastructure

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import logging
import sys

def next_higher_level(level: int):
    """
    Retrieves the level next to the given one.
    :param level: The level.
    :type level: int
    :return: The next level.
    :rtype: int
    """
    levels = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    for i, current_level in enumerate(levels):
        if level == current_level:
            return levels[i - 1] if i > 0 else current_level
    return level

def configure_logging(info:bool, debug:bool, quiet:bool):
    """
    Configures the logging system.
    :param info: Whether informational messages are allowed.
    :type info: bool
    :param debug: Whether to enable verbosity.
    :type debug: bool
    :param quiet: Whether to turn on "quiet mode".
    :type quiet: bool
    """
    level = logging.WARNING
    if quiet:
        level = logging.ERROR
    elif debug:
        level = logging.DEBUG
    elif info:
        level = logging.INFO
    default_logger = logging.getLogger()
    handlers_to_remove = []
    for handler in default_logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handlers_to_remove.append(handler)
    for handler in handlers_to_remove:
        default_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    default_logger.setLevel(level)
    default_logger.addHandler(console_handler)
    default_level = default_logger.getEffectiveLevel()

    next_level = next_higher_level(default_level)

    pythoneda_logger = logging.getLogger("pythoneda")
    pythoneda_logger.setLevel(default_level)

    for name in [ "asyncio", "git", "urllib3.connectionpool" ]:
        logger = logging.getLogger(name)
        logger.setLevel(next_level)
