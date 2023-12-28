"""
pythoneda/infrastructure/cli/cli_handler.py

This file defines the CliHandler class.

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
import abc
import argparse
from .abstract_cli_handler import AbstractCliHandler


class CliHandler(AbstractCliHandler, abc.ABC):

    """
    Base class for CLI handlers.

    Class name: CliHandler

    Responsibilities:
        - Handles the CLI based on certain criteria.

    Collaborators:
        - pythoneda.application.PythonEDA: They are notified back with the information retrieved from the command line.
    """

    def __init__(self, description: str):
        """
        Creates a new CliHandler.
        :param description: The description.
        :type description: str
        """
        super().__init__(description)

    async def entrypoint(self, app):
        """
        Receives the notification that the system has been accessed from the CLI.
        :param app: The PythonEDA instance.
        :type app: pythoneda.application.PythonEDA
        """
        args, unknown_args = self.parser.parse_known_args()
        await self.handle(app, args)

    @abc.abstractmethod
    async def handle(self, app, args: argparse.Namespace):
        """
        Processes the command specified from the command line.
        :param app: The PythonEDA instance.
        :type app: pythoneda.application.PythonEDA
        :param args: The CLI args.
        :type args: argparse.Namespace
        """
        raise NotImplementedError(
            f"'async def handle(self, app, args)' needs to be implemented in {self.__class__}"
        )
