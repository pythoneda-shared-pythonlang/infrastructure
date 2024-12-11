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
from dbus_next import BusType, Message, MessageType
from dbus_next.aio import MessageBus
from dbus_next.errors import SignatureBodyMismatchError
from .dbus_event import DbusEvent
from .dbus_signals import DbusSignals
from pythoneda.shared import attribute, Event, EventEmitter
from typing import Dict, Type


class DbusSignalEmitter(EventEmitter):
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

    def __init__(self, dbusEventsPackage: str):
        """
        Creates a new DbusSignalEmitter instance.
        :params dbusEventsPackage: The package with the d-bus events.
        :type dbusEventsPackage: str
        """
        super().__init__()
        self._signals = DbusSignals(dbusEventsPackage)

    @property
    @attribute
    def signals(self) -> DbusSignals:
        """
        Retrieves the d-bus signals.
        :return: The DbusSignals instance.
        :rtype: pythoneda.shared.infrastructure.dbus.DbusSignals
        """
        return self._signals

    def signal_emitters(self) -> Dict[str, Type[DbusEvent]]:
        """
        Retrieves the configured event emitters.
        :return: For each event, the d-bus implementation.
        :rtype: Dict[str, Type[pythoneda.shared.infrastructure.dbus.DbusEvent]]
        """
        return self.signals.signals()

    async def emit(self, event: Event):
        """
        Emits given event as d-bus signal.
        :param event: The domain event to emit.
        :type event: pythoneda.event.Event
        """
        collaborators = self.signal_emitters()

        if collaborators:
            event_class_name = self.__class__.full_class_name(event.__class__)
            if event_class_name in collaborators:
                impl_details = collaborators[event_class_name]
                instance_class = impl_details[0]
                instance = instance_class()
                path = instance.build_path(event)
                bus_type = impl_details[1]
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
