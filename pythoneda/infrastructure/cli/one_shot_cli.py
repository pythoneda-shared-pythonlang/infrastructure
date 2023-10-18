"""
pythoneda/infrastructure/cli/one_shot_cli.py

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
import argparse
from pythoneda import BaseObject, PrimaryPort
from pythoneda.shared.artifact_changes import Change
from pythoneda.shared.artifact_changes.events import StagedChangesCommitted
from pythoneda.shared.git import GitCommit, GitDiff, GitRepo
import sys

class OneShotCli(BaseObject, PrimaryPort):

    """
    A PrimaryPort to define the option not to listen for future events.

    Class name: OneShotCli

    Responsibilities:
        - Parse the command-line to check if the user wants to avoid listening to future events.

    Collaborators:
        - PythonEDA subclasses: They are notified back with the information retrieved from the command line.
    """

    async def accept(self, app):
        """
        Processes the command specified from the command line.
        :param app: The PythonEDA instance.
        :type app: PythonEDA
        """
        parser = argparse.ArgumentParser(description="Prevents listening to future events")
        parser.add_argument(
            "-1", "--one-shot", action="store_true", required=False, help="The repository folder"
        )
        args, unknown_args = parser.parse_known_args()

        await app.accept_one_shot(args.one_shot)
