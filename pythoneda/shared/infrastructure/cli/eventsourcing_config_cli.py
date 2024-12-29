# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/cli/eventsourcing_config_cli.py

This file provides event-sourcing configuration to the PythonEDA application.

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
from .abstract_cli_handler import AbstractCliHandler
from argparse import ArgumentParser, Namespace
from pythoneda.shared import PrimaryPort, PythonedaApplication
from typing import Union


class EventsourcingConfigCli(AbstractCliHandler, PrimaryPort):
    """
    A PrimaryPort that configures event-sourcing from the command line.

    Class name: EventsourcingConfigCli

    Responsibilities:
        - Interpret the event-sourcing settings provided via CLI, if any.

    Collaborators:
        - pythoneda.application.PythonEDA: Gets notified back with the interpreted event-sourcing settings.
    """

    def __init__(self):
        """
        Creates a new EventsourcingConfigCli instance.
        """
        super().__init__("Configures event-sourcing")

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
            "-es-p",
            "--eventsourcing-persistence",
            required=False,
            help="The EventSourcing persistence mechanism",
        )
        parser.add_argument(
            "-es-esdb-u",
            "--eventsourcing-eventstoredb-url",
            required=False,
            help="The EventStoreDB url",
        )
        parser.add_argument(
            "-es-esdb-r-c-f",
            "--eventsourcing-eventstoredb-root-certificates-file",
            required=False,
            help="The file with the EventStoreDB root certificates",
        )

    def entrypoint(self, app: PythonedaApplication):
        """
        Receives the notification that the system has been accessed from the CLI.
        :param app: The PythonEDA instance.
        :type app: pythoneda.shared.PythonedaApplication
        """
        args, unknown_args = self.parser.parse_known_args()
        self.handle(app, args)

    def handle(self, app: PythonedaApplication, args: Namespace):
        """
        Processes the command specified from the command line.
        :param app: The PythonEDA instance.
        :type app: pythoneda.shared.PythonedaApplication
        :param args: The CLI args.
        :type args: argparse.args
        """
        config = {}
        if args.es_p:
            config["PERSISTENCE_MODULE"] = args.es_p
        if args.es_esdb_u:
            config["EVENTSTOREDB_URI"] = args.es_esdb_u
        root_certificates = None
        if args.es_esdb_r_c_f:
            root_certificates = self.read_file(args.es_esdb_r_c_f)
            if not root_certificates:
                raise Exception(f"Could not read file {args.es_esdb_r_c_f}")
        if root_certificates:
            config["EVENTSTOREDB_ROOT_CERTIFICATES"] = root_certificates
        app.accept_configure_eventsourcing(config)

    def read_file(self, filePath: str) -> Union[bool, None]:
        """
        Reads given file if possible. Otherwise return None.
        :param filePath: The file path.
        :type filePath: str
        :return: The file contents, or None if the file could not be read.
        :rtype: Union[bool, None]
        """
        try:
            # Attempt to open the file in read mode
            with open(file_path, "r") as file:
                # Read the contents of the file
                contents = file.read()
                return contents
        except IOError:
            # If the file cannot be read (e.g., not found, no read permissions), return None
            return None


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
