# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/dbus/dbus_signals.py

This file defines the DbusSignals class.

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
from abc import ABCMeta
from dbus_next import BusType
import importlib
import inspect
import pkgutil
from pythoneda.shared import BaseObject, Event
from pythoneda.shared.infrastructure.dbus import DbusEvent
import pkgutil
from typing import Dict, Type


class DbusSignals(BaseObject):
    """
    Provides listening and emitting support for dynamically-discovered d-bus events.

    Class name: DbusSignals

    Responsibilities:
        - Discover d-bus events dynamically.
        - Support for listening and emitting discovered d-bus events.

    Collaborators:
        - pythoneda.shared.Event
    """

    def __init__(self, package: str):
        """
        Creates a new DbusSignals instance to discover events in given package.
        :param package: The package to analyze.
        :type package: str
        """
        super().__init__()
        self._package = package

    @property
    def package(self) -> str:
        """
        Retrieves the package with the events.
        :return: Such package.
        :rtype: str
        """
        return self._package

    def find_subclasses_in_package(self, package_name, base_class):
        result = []

        package_spec = importlib.util.find_spec(package_name)
        if package_spec is not None and package_spec.submodule_search_locations:
            subclasses = []

            for importer, modname, ispkg in pkgutil.walk_packages(
                package_spec.submodule_search_locations
            ):
                full_module_name = f"{package_name}.{modname}"
                try:
                    module = importlib.import_module(full_module_name)
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if (
                            issubclass(obj, base_class)
                            and obj is not base_class
                            and not inspect.isabstract(obj)
                        ):
                            subclasses.append(obj)
                except ImportError:
                    DbusSignals.logger().error(
                        f"Could not import module {full_module_name}."
                    )

            for subclass in subclasses:
                result.append(subclass)
                for child in subclass.__subclasses__():
                    result.extend(self.find_subclasses_in_package(package_name, child))
        else:
            DbusSignals.logger().error(f"Could not find the package '{package_name}'.")
            result = []

        return result

    def signals(self) -> Dict[str, Type[DbusEvent]]:
        """
        Retrieves the configured signals.
        :return: For each event class, the event interface.
        :rtype: Dict[str, Type[pythoneda.shared.infrastructure.dbus.DbusEvent]]
        """
        result = {}
        dbus_event_classes = self.find_subclasses_in_package(self.package, DbusEvent)

        for dbus_event_class in dbus_event_classes:
            key = self.__class__.full_class_name(dbus_event_class.event_class())
            result[key] = dbus_event_class

        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
