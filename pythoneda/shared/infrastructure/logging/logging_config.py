# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/logging/logging_config.py

This file configures PythonEDA logging.

Copyright (C) 2023-today rydnr's pythoneda-shared/infrastructure

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
from datetime import datetime
import logging
from pythoneda.shared import Invariant, Invariants, PythonedaApplication
import sys


def next_higher_level(level: int):
    """
    Retrieves the level next to the given one.
    :param level: The level.
    :type level: int
    :return: The next level.
    :rtype: int
    """
    levels = [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    ]
    for i, current_level in enumerate(levels):
        if level == current_level:
            return levels[i - 1] if i > 0 else current_level
    return level


def configure_logging(info: bool, debug: bool, trace: bool, quiet: bool):
    """
    Configures the logging system.
    :param info: Whether the info level is enabled.
    :type info: bool
    :param debug: Whether debug messages are allowed.
    :type debug: bool
    :param trace: Whether to maximize verbosity.
    :type trace: bool
    :param quiet: Whether to turn on "quiet mode".
    :type quiet: bool
    """
    level = logging.WARNING
    if quiet:
        level = logging.ERROR
    elif trace:
        level = logging.TRACE
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
    invariant_app = Invariants.instance().apply(PythonedaApplication.invariant_type)
    if invariant_app is None:
        formatter = TruncateCategoryFormatter(
            f"[!!] %(asctime)s - %(name)s %(funcName)s:%(lineno)d%(lineno)d - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        formatter = TruncateCategoryFormatter(
            f"[{invariant_app.value.name}] %(asctime)s - %(name)s %(funcName)s:%(lineno)d - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    console_handler.setFormatter(formatter)
    default_logger.setLevel(level)
    default_logger.addHandler(console_handler)
    default_level = default_logger.getEffectiveLevel()

    next_level = next_higher_level(default_level)

    pythoneda_logger = logging.getLogger("pythoneda")
    pythoneda_logger.setLevel(default_level)

    for name in ["asyncio", "git", "urllib3.connectionpool"]:
        logger = logging.getLogger(name)
        logger.setLevel(next_level)


class TruncateCategoryFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, max_category_length=30):
        super().__init__(fmt, datefmt)
        self.max_category_length = max_category_length

    def truncate_category(self, category):
        """
        Truncate the category to fit within the maximum length, keeping the last token.
        """
        tokens = category.split(".")
        truncated = tokens[-1]  # Start with the last token
        for token in reversed(tokens[:-1]):
            candidate = f"{token}.{truncated}"
            if len(candidate) > self.max_category_length:
                break
            truncated = candidate
        if len(truncated) < len(category):
            truncated = f"...{truncated}"
        return truncated

    def format(self, record):
        # Truncate the logger name (which serves as the category)
        record.name = self.truncate_category(record.name)
        return super().format(record)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
