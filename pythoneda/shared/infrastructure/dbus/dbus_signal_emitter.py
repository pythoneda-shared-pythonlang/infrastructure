# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/dbus/dbus_signal_emitter.py

This file defines the DbusSignalEmitter class.

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
from dbus_next.aio import MessageBus
from dbus_next import BusType, Message, MessageType
from pythoneda.shared import Event, EventEmitter
from typing import Dict


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

    def __init__(self):
        """
        Creates a new DbusSignalEmitter instance.
        """
        super().__init__()

    def signal_emitters(self) -> Dict:
        """
        Retrieves the configured event emitters.
        :return: For each event, a list with the event interface and the bus type.
        :rtype: Dict
        """
        return {}

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
                interface_class, bus_type = collaborators[event_class_name]
                instance = interface_class()
                bus = await MessageBus(bus_type=bus_type).connect()
                bus.export(interface_class.path(), instance)
                await bus.send(
                    Message.new_signal(
                        interface_class.path(),
                        self.__class__.full_class_name(interface_class),
                        instance.name,
                        instance.sign(event),
                        instance.transform(event),
                    )
                )
                DbusSignalEmitter.logger().info(
                    f"Sent signal {interface_class.__module__}.{interface_class.__name__} on path {interface_class.path()} to d-bus {bus_type}"
                )
            else:
                DbusSignalEmitter.logger().warn(
                    f"No d-bus emitter registered for event {event.__class__}"
                )
        else:
            DbusSignalEmitter.logger().warn(f"No d-bus emitters found")
        await super().emit(event)
# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
