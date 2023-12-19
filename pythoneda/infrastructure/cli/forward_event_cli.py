"""
pythoneda/infrastructure/cli/forward_event_cli.py

This file defines the ForwardEventCli class.

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
import abc
import argparse
from pythoneda import Event, EventEmitter, listen, Ports


class ForwardEventCli(CliHandler, abc.ABC):

    """
    A CLI handler that forwards events.

    Class name: ForwardEventCli

    Responsibilities:
        - Build events from information from the CLI, and forwards them.

    Collaborators:
        - pythoneda.application.PythonEDA: To initialize this class.
    """

    _singleton = None

    def __init__(self, description: str):
        """
        Creates a new CliHandler.
        :param description: The description.
        :type description: str
        """
        super().__init__(description)
        print("in init")

    @classmethod
    @property
    def is_one_shot_compatible(cls) -> bool:
        """
        Returns True to indicate this port is compatible with the "one-shot" behavior.
        :return: True always.
        :rtype: bool
        """
        return True

    async def handle(self, app, args: argparse.Namespace):
        """
        Receives the notification that the system has been accessed from the CLI.
        :param app: The PythonEDA instance.
        :type app: pythoneda.application.PythonEDA
        :param args: The CLI args.
        :type args: argparse.Namespace
        """
        args, unknown_args = self.parser.parse_known_args()
        event = self.build_event(app, args)
        print(f"event -> {event}")
        if event is not None:
            await self.emit_event(event)

    @abc.abstractmethod
    def build_event(self, app, args: argparse.Namespace) -> Event:
        """
        Builds an event from the information specified from the command line.
        :param app: The PythonEDA instance.
        :type app: pythoneda.application.PythonEDA
        :param args: The CLI args.
        :type args: argparse.Namespace
        :return: The event.
        :rtype: pythoneda.Event
        """
        raise NotImplementedError(
            f"'def build_event(self, app, args)' needs to be implemented in {self.__class__}"
        )

    async def emit_event(cls, event: Event):
        """
        Emits given event.
        :param event: The event.
        :type event: pythoneda.Event
        """
        event_emitter = Ports.instance().resolve(EventEmitter)
        if event_emitter is not None:
            ForwardEventCli.logger().debug(f"Emitting {event.__class__}")
            await event_emitter.emit(event)
