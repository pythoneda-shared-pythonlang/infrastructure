# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/dbus/dbus_signal_emitter.py

This file defines the DbusSignalEmitter class.

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
from dbus_next import BusType, Message, MessageType
from dbus_next.aio import MessageBus
from dbus_next.errors import SignatureBodyMismatchError
from .dbus_event import DbusEvent
from .dbus_signals import DbusSignals
from pythoneda.shared import attribute, Event, EventEmitter
from typing import Dict, List, Tuple, Type


class DbusSignalEmitter(EventEmitter, abc.ABC):
    """
    A Port that emits events as d-bus signals.

    Class name: DbusSignalEmitter

    Responsibilities:
        - Connect to d-bus.
        - Translate domain events to d-bus signals.

    Collaborators:
        - pythoneda.shared.application.PythonEDA: Requests emitting events.
    """

    _count = 0
    _events = None
    _events_by_class = {}

    def __init__(self):
        """
        Creates a new DbusSignalEmitter instance.
        """
        super().__init__()

    @classmethod
    def enable(cls, *args: Tuple, **kwargs: Dict):
        """
        Enables this port.
        :param args: Additional positional arguments.
        :type args: Tuple
        :param kwargs: Additional keyword arguments.
        :type kwargs: Dict
        """
        super().enable(*args, **kwargs)
        cls._events = kwargs.get("events", None)
        event_pkgs = cls.event_packages()
        if cls._events is None and event_pkgs is not None:
            cls._events = []
            for pkg in event_pkgs:
                for signal_name, value in DbusSignals(pkg).signals():
                    cls._events.append({"event-class": value[0], "bus-type": value[1]})
                    cls._events_by_class[cls.full_class_name(value[0])] = value[1]
        else:
            for event_details in cls._events:
                event_class = event_details.get("event-class", None)
                cls._events_by_class[cls.full_class_name(event_class.event_class())] = {
                    "event-class": event_class,
                    "bus-type": event_details.get("bus-type", BusType.SYSTEM),
                }

    @classmethod
    @abc.abstractmethod
    def event_packages(cls) -> List[str]:
        """
        Retrieves the packages of the supported events.
        :return: The packages.
        :rtype: List[str]
        """
        pass

    async def emit(self, event: Event):
        """
        Emits given event as d-bus signal.
        :param event: The domain event to emit.
        :type event: pythoneda.event.Event
        """
        if self._events:
            event_class_name = self.__class__.full_class_name(event.__class__)
            print(
                f"Event class name: {event_class_name}, events_by_class: {self._events_by_class}"
            )
            event_details = self._events_by_class.get(event_class_name, None)
            if event_details is not None:
                instance_class = event_details.get("event-class", None)
                instance = instance_class()
                path = instance.build_path(event)
                bus_type = event_details.get("bus-type", BusType.SYSTEM)
                bus = await MessageBus(bus_type=bus_type).connect()
                bus.export(path, instance)
                try:
                    await bus.send(
                        Message.new_signal(
                            path,
                            self.__class__.full_class_name(instance_class),
                            instance.name,
                            instance.sign(event),
                            instance.transform(event),
                        )
                    )
                    DbusSignalEmitter.logger().info(
                        f"Sent signal {instance_class.__module__}.{instance_class.__name__} on path {path} to d-bus {bus_type}"
                    )
                except SignatureBodyMismatchError as mismatch:
                    DbusSignalEmitter.logger().error(
                        f"Bad implementation of class {event.__class__}: {mismatch}"
                    )
                    DbusSignalEmitter.logger().error(mismatch)

            else:
                DbusSignalEmitter.logger().warning(
                    f"No d-bus emitter registered for event {event.__class__} ({event})"
                )
        else:
            DbusSignalEmitter.logger().warning(f"No d-bus emitters found")

        return await super().emit(event)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
