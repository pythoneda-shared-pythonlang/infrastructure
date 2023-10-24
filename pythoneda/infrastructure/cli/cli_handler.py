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
from pythoneda import BaseObject
import sys

class CliHandler(BaseObject, abc.ABC):

    """
    Base class for CLI handlers.

    Class name: CliHandler

    Responsibilities:
        - Handles the CLI based on certain criteria.

    Collaborators:
        - pythoneda.application.PythonEDA: They are notified back with the information retrieved from the command line.
    """

    def __init__(self, app):
        """
        Creates a new CliHandler.
        :param app: The PythonEDA application.
        :rtype: pythoneda.application.PythonEDA
        """
        super().__init__()
        self._app = app

    @property
    def app(self):
        """
        Retrieves the PythonEDA instance.
        :return: Such instance.
        :rtype: pythoneda.application.PythonEDA
        """
        return self._app

    @abc.abstractmethod
    async def handle(self, args):
        """
        Processes the command specified from the command line.
        :param args: The CLI args.
        :type args: argparse.args
        """
        raise NotImplementedError("'async def handle(self, args)' needs to be implemented in subclasses")
