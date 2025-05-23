# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/cli/logging_config_cli.py

This file parses the logging config from the command-line interface for PythonEDA-Application base.

Copyright (C) 2023-today rydnr's pythoneda-shared-pythonlang/infrastructure

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
from .cli_handler import CliHandler
from argparse import ArgumentParser, Namespace
from pythoneda.shared import PrimaryPort, PythonedaApplication
from typing import Dict


class LoggingConfigCli(CliHandler, PrimaryPort):
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
        super().__init__("Logging")

    @classmethod
    def priority(cls) -> int:
        """
        Provides the priority information.
        :return: Such priority.
        :rtype: int
        """
        return 0

    @classmethod
    @property
    def is_one_shot_compatible(cls) -> bool:
        """
        Returns True to indicate this port is compatible with the "one-shot" behavior.
        :return: True always.
        :rtype: bool
        """
        return True

    def add_arguments(self, parser: ArgumentParser):
        """
        Defines the specific CLI arguments.
        :param parser: The parser.
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument(
            "-v", "--debug", action="store_true", help="Enable debug mode"
        )
        parser.add_argument(
            "-vv", "--trace", action="store_true", help="Enable trace mode"
        )
        parser.add_argument(
            "-q", "--quiet", action="store_true", help="Enable quiet mode"
        )

    async def handle(self, app: PythonedaApplication, args):
        """
        Processes the command specified from the command line.
        :param app: The PythonEDA instance.
        :type app: pythoneda.shared.PythonedaApplication
        :param args: The CLI args.
        :type args: argparse.args
        """
        info = True
        debug = args.debug
        trace = args.trace
        if args.quiet:
            info = False
            debug = False
            trace = False
        app.accept_configure_logging(
            {
                "trace": trace,
                "debug": debug,
                "info": info,
                "quiet": args.quiet,
            }
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
