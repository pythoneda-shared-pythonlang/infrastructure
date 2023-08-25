"""
pythoneda/infrastructure/dbus/dbus_signal_listener.py

This file defines the DbusSignalListener class.

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
import abc
import asyncio
from dbus_next.aio import MessageBus
from dbus_next import BusType, Message, MessageType
from pythoneda import EventListenerPort
from typing import Dict

class DbusSignalListener(EventListenerPort, abc.ABC):
    """
    A PrimaryPort that receives events as d-bus signals.

    Class name: DbusSignalListener

    Responsibilities:
        - Connect to d-bus.
        - Translate d-bus signals to domain events.

    Collaborators:
        - PythonEDAApplication: Gets notified back with domain events.
    """
    def __init__(self):
        """
        Creates a new DbusSignalListener instance.
        """
        super().__init__()

    def priority(self) -> int:
        """
        Provides the priority information.
        :return: Such priority.
        :rtype: int
        """
        return 100

    async def set_app(self, app):
        """
        Specifies the PythoneEDA instance.
        :param app: The PythonEDA instance.
        :type app: PythonEDA from pythonedaapplication.pythoneda
        """
        self._app = app

    @property
    def app(self):
        """
        Retrieves the PythoneEDA instance.
        :return: The PythonEDA instance.
        :rtype: PythonEDA from pythonedaapplication.pythoneda
        """
        return self._app

    def signal_receivers(self, app) -> Dict:
        """
        Retrieves the configured signal receivers.
        :param app: The PythonEDA instance.
        :type app: PythonEDA from pythonedaapplication.pythoneda
        :return: A dictionary with the signal name as key, and the tuple interface and bus type as the value.
        :rtype: Dict
        """
        return {}

    async def accept(self, app):
        """
        Receives the notification to connect to d-bus.
        :param app: The PythonEDAApplication instance.
        :type app: PythonEDA from pythonedaapplication.pythoneda
        """
        await self.set_app(app)

        receivers = self.signal_receivers(app).items()

        if receivers:
            for signal_name, value in receivers:
                interface_class, bus_type = value
                interface = interface_class()

                fqdn_interface_class = self.__class__.fqdn_key(interface_class)
                bus = await MessageBus(bus_type=BusType.SYSTEM).connect()

                bus.add_message_handler(self.process_message)

                # Subscribe to the signal
                await bus.call(
                    Message(
                        destination='org.freedesktop.DBus',
                        path='/org/freedesktop/DBus',
                        interface='org.freedesktop.DBus',
                        member='AddMatch',
                        signature='s',
                        body=[f"type='signal',interface='{fqdn_interface_class}',path='{interface_class.path()}',member='{interface.name}'"]
                    )
                )
                DbusSignalListener.logger().info(f'Subscribed to signal {interface.name} via {interface_class.path()}')

            while True:
                await asyncio.sleep(1)
        else:
            DbusSignalListener.logger().warning(f'No receivers configured for {app}!')

    def process_message(self, message: Message) -> bool:
        """
        Process an incoming message.
        :param message: The message.
        :type message: dbus_next.Message
        :return: True, to avoid replying.
        :rtype: bool
        """
        if message.message_type == MessageType.SIGNAL:
            DbusSignalListener.logger().info(f'Received signal {message.member}')
            result = True
            event = self.parse(message, message.member)
            asyncio.create_task(self.listen(event))
        else:
            result = False

        return result

    def _camel_to_snake(self, name:str) -> str:
        """
        Converts camel case to snake case.
        :param name: The name in camel case.
        :type name: str
        :return: The snake case version.
        :rtype: str
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @abc.abstractmethod
    def event_package(self):
        """
        Retrieves the event package.
        :return: The package.
        :rtype: str
        """
        raise NotImplementedError("event_package() should be implemented in subclasses")

    def parse(self, message: Message, signal:str):
        """
        Parses given signal.
        :param message: The message.
        :type message: dbus_next.Message
        :param signal: The name of the signal.
        :type signal: str
        """
        result = None
        package = self.event_package()
        # check the package matches "pythoneda.realm.rydnr.events"
        if signal.split("_")[:-1] == package.split("."):
            # delegate the parsing logic to the dbus event class
            from importlib import import_module
            module = import_module(f'{package}.infrastructure.dbus_{self._camel_to_snake(signal.split("_")[-1])}')
            dbus_event_class = getattr(module, f'Dbus{signal.split("_"[-1])}')
            result = dbus_event_class.parse(message)
        return result

    async def listen(self, event):
        """
        Gets notified of a signal.
        :param event: The event.
        :type event: pythoneda.event.Event
        """
        await self.app.accept(event)
