# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/cli/cli_handler.py

This file defines the CliHandler class.

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
import abc
from .abstract_cli_handler import AbstractCliHandler
import argparse
from pythoneda.shared import PythonedaApplication
from typing import Dict, Union


class CliHandler(AbstractCliHandler, abc.ABC):
    """
    Base class for CLI handlers.

    Class name: CliHandler

    Responsibilities:
        - Handles the CLI based on certain criteria.

    Collaborators:
        - pythoneda.application.PythonEDA: They are notified back with the information retrieved from the command line.
    """

    _cli_already_handled = False

    def __init__(self, description: str, scope: Union[str, None] = None):
        """
        Creates a new CliHandler.
        :param description: The description.
        :type description: str
        :param scope: The scope of the handler.
        :type scope: Union[str, None]
        """
        super().__init__(description, scope)

    async def configure(self):
        """
        Configures the port.
        """
        if self.scope is None:
            self._actual_parser = self.parser
        else:
            self._actual_parser = self._subparsers.add_parser(
                self.scope, help=self.description
            )
        self.add_arguments(self.actual_parser)
        self.actual_parser.set_defaults(func=self.handle)

    async def entrypoint(self, app: PythonedaApplication):
        """
        Receives the notification that the system has been accessed from the CLI.
        :param app: The PythonEDA instance.
        :type app: pythoneda.shared.PythonedaApplication
        """
        if not self._cli_already_handled:
            self._cli_already_handled = True
            args, unknown_args = self.parser.parse_known_args()
            await args.func(app, args)

    @abc.abstractmethod
    async def handle(self, app: PythonedaApplication, args: argparse.Namespace):
        """
        Processes the command specified from the command line.
        :param app: The PythonEDA instance.
        :type app: pythoneda.shared.PythonedaApplication
        :param args: The CLI args.
        :type args: argparse.Namespace
        """
        raise NotImplementedError(
            f"'async def handle(self, app, args)' needs to be implemented in {self.__class__}"
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
