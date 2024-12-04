# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/dbus/dbus_signal_listener.py

This file defines the DbusSignalListener class.

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
import asyncio
from dbus_next.aio import MessageBus
from dbus_next import BusType, Message, MessageType
from .dbus_event import DbusEvent
from .dbus_signals import DbusSignals
from pythoneda.shared import attribute, EventListenerPort
from typing import Dict, List, Type


class DbusSignalListener(EventListenerPort):
    """
    A PrimaryPort that receives events as d-bus signals.

    Class name: DbusSignalListener

    Responsibilities:
        - Connect to d-bus.
        - Translate d-bus signals to domain events.

    Collaborators:
        - pythoneda.shared.application.PythonEDA: Gets notified back with domain events.
    """

    def __init__(self, dbusEventsPackage: str):
        """
        Creates a new DbusSignalListener instance.
        :params dbusEventsPackage: The package with the d-bus events.
        :type dbusEventsPackage: str
        """
        super().__init__()
        self._app = None
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

    @classmethod
    def priority(cls) -> int:
        """
        Provides the priority information.
        :return: Such priority.
        :rtype: int
        """
        return 100

    async def set_app(self, app):
        """
        Specifies the PythonEDA instance.
        :param app: The PythonEDA instance.
        :type app: pythoneda.application.PythonEDA
        """
        self._app = app

    @property
    def app(self):
        """
        Retrieves the PythonEDA instance.
        :return: The PythonEDA instance.
        :rtype: pythoneda.application.pythonEDA
        """
        return self._app

    def signal_receivers(self, app) -> Dict[str, Type[DbusEvent]]:
        """
        Retrieves the configured signal receivers.
        :param app: The PythonEDA instance.
        :type app: pythoneda.application.PythonEDA
        :return: For each event, the d-bus implementation.
        :rtype: Dict[str, Type[pythoneda.shared.infrastructure.dbus.DbusEvent]]
        """
        return self.signals.signals()

    def parse_signal_name(self, value) -> List:
        """
        Parses a signal name into tokens.
        :param value: The value.
        :type value: str
        :return: The tokens.
        :rtype: List
        """
        result = []
        tokens = value.split("_")
        current_token = None
        for token in tokens:
            if token[0].isupper():
                if current_token is not None:
                    result.append("_".join(current_token))
                result.append(token)
                current_token = None
            else:
                if current_token is None:
                    current_token = []
                current_token.append(token)

        if current_token is not None:
            result.append("_".join(current_token))

        result[:-1] = [x.lower() for x in result[:-1]]

        return result

    async def entrypoint(self, app):
        """
        Receives the notification to connect to d-bus.
        :param app: The PythonEDAApplication instance.
        :type app: pythoneda.application.PythonEDA
        """
        await self.set_app(app)

        receivers = self.signal_receivers(app).items()

        if receivers:
            for signal_name, value in receivers:
                interface_class = value[0]
                instance = interface_class()

                fqdn_interface_class = self.__class__.full_class_name(interface_class)
                bus = await MessageBus(bus_type=value[1]).connect()

                bus.add_message_handler(self.process_message)

                # Subscribe to the signal
                await bus.call(
                    Message(
                        destination="org.freedesktop.DBus",
                        path="/org/freedesktop/DBus",
                        interface="org.freedesktop.DBus",
                        member="AddMatch",
                        signature="s",
                        body=[
                            f"type='signal',interface='{fqdn_interface_class}',path='{instance.path}',member='{instance.name}'"
                        ],
                    )
                )
                DbusSignalListener.logger().debug(
                    f"Subscribed to signal {instance.name} via {instance.path}"
                )

            while True:
                await asyncio.sleep(1)
        else:
            DbusSignalListener.logger().warning(f"No receivers configured for {app}!")

    def process_message(self, message: Message) -> bool:
        """
        Process an incoming message.
        :param message: The message.
        :type message: dbus_next.Message
        :return: True, to avoid replying.
        :rtype: bool
        """
        if message.message_type == MessageType.SIGNAL:
            DbusSignalListener.logger().info(f"Received signal {message.member}")
            result = True
            event = self.parse(message, message.member)
            if event:
                asyncio.create_task(self.listen(event))
            else:
                DbusSignalListener.logger().warning(
                    f"Discarding unparseable message: {message}"
                )

        else:
            result = False

        return result

    def parse(self, message: Message, signal: str):
        """
        Parses given signal.
        :param message: The message.
        :type message: dbus_next.Message
        :param signal: The name of the signal.
        :type signal: str
        """
        result = None

        tokens = self.parse_signal_name(signal)
        package = ".".join(tokens[:-1])
        # delegate the parsing logic to the dbus event class
        from importlib import import_module

        module_name = f"{package}.infrastructure.dbus.dbus_{self.__class__.camel_to_snake(tokens[-1])}"
        try:
            module = import_module(module_name)
            dbus_event_class = getattr(module, f"Dbus{tokens[-1]}")
            result = dbus_event_class.parse(message)
        except ImportError as err:
            DbusSignalListener.logger().debug(f"Discarding unparseable event: {err}")
        except Exception as err:
            DbusSignalListener.logger().error(err)

        return result

    async def listen(self, event):
        """
        Gets notified of a signal.
        :param event: The event.
        :type event: pythoneda.Event
        """
        DbusSignalListener.logger().debug(f"Received d-bus signal: {event}")
        await self.app.accept(event)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
