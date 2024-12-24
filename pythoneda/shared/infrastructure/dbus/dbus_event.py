# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/dbus/dbus_event.py

This file defines the DbusEvent class.

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
from dbus_next import BusType, Message
from dbus_next.service import ServiceInterface
import json
from pythoneda.shared import BaseObject, Event
from typing import List, Type


class DbusEvent(BaseObject, ServiceInterface, abc.ABC):
    """
    Abstract class for D-Bus events.

    Class name: DbusEvent

    Responsibilities:
        - Define the common logic for all d-bus events.

    Collaborators:
        - None
    """

    def __init__(self, name: str, path: str):
        """
        Creates a new DbusEvent.
        :param name: The signal name.
        :type name: str
        :param path: The d-bus path.
        :type path: str
        """
        super().__init__(name)
        self._path = path

    @property
    def path(self) -> str:
        """
        Retrieves the d-bus path.
        :return: Such value.
        :rtype: str
        """
        return self._path

    def build_path(self, event: Event) -> str:
        """
        Retrieves the d-bus path for given event.
        :param event: The event.
        :type event: pythoneda.shared.Event
        :return: Such value.
        :rtype: str
        """
        return self.path

    @classmethod
    @abc.abstractmethod
    def transform(cls, event: Event) -> List[str]:
        """
        Transforms given event to signal parameters.
        :param event: The event to transform.
        :type event: pythoneda.shared.Event
        :return: The event information.
        :rtype: List[str]
        """
        pass

    @classmethod
    @abc.abstractmethod
    def sign(cls, event: Event) -> str:
        """
        Retrieves the signature for the parameters of given event.
        :param event: The domain event.
        :type event: pythoneda.shared.Event
        :return: The signature.
        :rtype: str
        """
        pass

    @classmethod
    @abc.abstractmethod
    def event_class(cls) -> Type[Event]:
        """
        Retrieves the specific event class.
        :return: Such class.
        :rtype: type(pythoneda.shared.Event)
        """
        pass

    @classmethod
    @abc.abstractmethod
    def parse(cls, message: Message) -> Event:
        """
        Parses given d-bus message containing an event.
        :param message: The message.
        :type message: dbus_next.Message
        :return: The specific event.
        :rtype: pythoneda.shared.Event
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
#!/usr/bin/env python3
