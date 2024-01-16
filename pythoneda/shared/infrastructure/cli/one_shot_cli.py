# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/cli/one_shot_cli.py

This file defines the OneShotCli class.

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
from .cli_handler import CliHandler
from argparse import ArgumentParser
from pythoneda.shared import BaseObject, PrimaryPort


class OneShotCli(CliHandler, PrimaryPort):

    """
    A PrimaryPort to define the option not to listen for future events.

    Class name: OneShotCli

    Responsibilities:
        - Parse the command-line to check if the user wants to avoid listening to future events.

    Collaborators:
        - PythonEDA subclasses: They are notified back with the information retrieved from the command line.
    """

    def __init__(self):
        """
        Creates a new OneShotCli instance.
        """
        super().__init__("Prevents listening to future events")

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
            "-1",
            "--one-shot",
            action="store_true",
            required=False,
            help="The repository folder",
        )

    async def handle(self, app, args):
        """
        Processes the command specified from the command line.
        :param app: The PythonEDA instance.
        :type app: pythoneda.application.PythonEDA
        :param args: The CLI args.
        :type args: argparse.args
        """
        app.accept_one_shot(args.one_shot)
