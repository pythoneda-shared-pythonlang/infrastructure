"""
pythonedainfrastructure/pythonedacli/logging_config_cli.py

This file parses the logging config from the command-line interface for PythonEDA-Application base.

Copyright (C) 2023-today rydnr's pythoneda-infrastructure/base

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
from pythoneda.primary_port import PrimaryPort

import argparse

class LoggingConfigCli(PrimaryPort):

    """
    A PrimaryPort that configures logging the command line.

    Class name: LoggingConfigCli

    Responsibilities:
        - Interpret the logging settings provided via CLI, if any.
        - Configure the logging using the provided settings.

    Collaborators:
        - PythonEDAApplication: Gets notified back with the interpreted logging settings.
    """
    def __init__(self):
        """
        Creates a new LoggingConfigCli instance.
        """
        super().__init__()

    def priority(self) -> int:
        """
        Provides the priority information.
        :return: Such priority.
        :rtype: int
        """
        return 0

    async def accept(self, app):
        """
        Receives the notification that the system has been accessed from the CLI.
        :param app: The PythonEDAApplication instance.
        :type app: pythonedaapplication.PythonEDAApplication
        """
        parser = argparse.ArgumentParser(
            description="Catches logging flags from the command line"
        )
        parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose mode")
        parser.add_argument('-vv', '--trace', action='store_true', help="Enable tracing mode")
        parser.add_argument('-q', '--quiet', action='store_true', help="Enable quiet mode")
        args, unknown_args = parser.parse_known_args()
        await app.accept_configure_logging({ "verbose": args.verbose, "trace": args.trace, "quiet": args.quiet })
