# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/cli/abstract_cli_handler.py

This file defines the AbstractCliHandler class.

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
import argparse
from pythoneda.shared import BaseObject, PrimaryPort
from typing import Union


class AbstractCliHandler(PrimaryPort, BaseObject, abc.ABC):
    """
    Abstract base class for CLI handlers.

    Class name: AbstractCliHandler

    Responsibilities:
        - Provides parser and layout for subclasses.

    Collaborators:
        - pythoneda.application.PythonEDA: They are notified back with the information retrieved from the command line.
    """

    _parser = argparse.ArgumentParser(conflict_handler="resolve", add_help=True)
    _subparsers = _parser.add_subparsers(title="Events", dest="event", required=True)

    def __init__(self, description: str, scope: Union[str, None] = None):
        """
        Creates a new AbstractCliHandler.
        :param description: The description.
        :type description: str
        :param scope: The scope of the handler.
        :type scope: Union[str, None]
        """
        self._description = description
        self._scope = scope
        self._actual_parser = None
        super().__init__()

    @property
    def description(self) -> str:
        """
        Retrieves the handler description.
        :return: Such text.
        :rtype: str
        """
        return self._description

    @classmethod
    def instantiate(cls):
        """
        Creates an instance.
        :return: The new instance.
        :rtype: pythoneda.Port
        """
        return cls()

    @property
    def parser(self) -> argparse.ArgumentParser:
        """
        Retrieves the parser.
        :return: Such instance.
        :rtype: argparse.ArgumentParser
        """
        return self._parser

    @property
    def actual_parser(self) -> argparse.ArgumentParser:
        """
        Retrieves the actual parser.
        :return: Such instance.
        :rtype: argparse.ArgumentParser
        """
        return self._actual_parser

    @property
    def scope(self) -> Union[str, None]:
        """
        Retrieves the scope of this port.
        :return: The scope.
        :rtype: Union[str, None]
        """
        return self._scope

    @abc.abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser):
        """
        Defines the specific CLI arguments.
        :param parser: The parser.
        :type parser: argparse.ArgumentParser
        """
        pass


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
