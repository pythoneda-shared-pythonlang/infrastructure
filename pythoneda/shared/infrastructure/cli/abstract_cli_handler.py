# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/cli/abstract_cli_handler.py

This file defines the AbstractCliHandler class.

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
import abc
import argparse
from pythoneda.shared import BaseObject, PrimaryPort


class AbstractCliHandler(PrimaryPort, BaseObject, abc.ABC):

    """
    Abstract base class for CLI handlers.

    Class name: AbstractCliHandler

    Responsibilities:
        - Provides parser and layout for subclasses.

    Collaborators:
        - pythoneda.application.PythonEDA: They are notified back with the information retrieved from the command line.
    """

    def __init__(self, description: str):
        """
        Creates a new AbstractCliHandler.
        :param description: The description.
        :type description: str
        """
        super().__init__()
        self._parser = argparse.ArgumentParser(description=description)
        self.add_arguments(self._parser)

    @property
    def parser(self) -> argparse.ArgumentParser:
        """
        Retrieves the parser.
        :return: Such instance.
        :rtype: argparse.ArgumentParser
        """
        return self._parser

    @abc.abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser):
        """
        Defines the specific CLI arguments.
        :param parser: The parser.
        :type parser: argparse.ArgumentParser
        """
        pass
