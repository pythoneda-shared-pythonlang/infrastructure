# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/logging/logging_adapter.py

This file configures PythonEDA to use the default Python logging.

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
import logging
from pythoneda.shared import BaseObject, LoggingPort


class LoggingAdapter(LoggingPort, BaseObject):
    """
    Adapter of Python logging to PythonEDA's LoggingPort.

    Class name: LoggingAdapter

    Responsibilities:
        - Provides logging through standard Python logging.

    Collaborators:
        - logging: The default Python logging mechanism.
    """

    def __init__(self):
        """
        Creates a new instance.
        """
        super().__init__()

    def logger(self, category: str):
        """
        Retrieves the logger instance.
        :param category: The logging category.
        :type category: str
        :return: Such instance.
        :rtype: logging.Logger
        """
        return logging.getLogger(category)
