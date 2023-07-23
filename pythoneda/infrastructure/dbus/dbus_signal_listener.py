"""
pythonedainfrastructure/pythonedacli/logging_config_cli.py

This file defines the DbusSignalListener class.

Copyright (C) 2023-today rydnr's pythoneda-infrastructure/base

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
from pythoneda.primary_port import PrimaryPort

import abc
import asyncio
from dbus_next.aio import MessageBus
from dbus_next import BusType, Message, MessageType

from typing import Dict

class DbusSignalListener(PrimaryPort, abc.ABC):

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
        print(f'Accepting app {app}')
        await self.set_app(app)

        receivers = self.signal_receivers(app).items()

        if receivers:
            print(f'receivers: {receivers}')
            for signal_name, value in receivers:
                interface_class, bus_type = value
                interface = interface_class()

                fqdn_interface_class = self.fqdn_key(interface_class)
                bus = await MessageBus(bus_type=BusType.SYSTEM).connect()

                bus.add_message_handler(self.process_message)

                print(f'Subscribing to signal {interface.name}, interface {fqdn_interface_class}, path {interface_class.path()}')
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

            while True:
                await asyncio.sleep(1)
        else:
            logging.getLogger(self.__class__).warning(f'No receivers configured for {app}!')

    def fqdn_key(self, cls: type) -> str:
        """
        Retrieves the key used for given class.
        :param cls: The class.
        :type cls: Class
        :return: The key.
        :rtype: str
        """
        return f'{cls.__module__}.{cls.__name__}'

    def process_message(self, message: Message) -> bool:
        """
        Process an incoming message.
        :param message: The message.
        :type message: dbus_next.Message
        :return: True, to avoid replying.
        :rtype: bool
        """
        if message.message_type == MessageType.SIGNAL:
            print(f'Received signal {message.member}')
            result = True
            parsing = f'parse_{message.member}'
            parsing_handler = getattr(self, parsing)
            event = parsing_handler(message)
            listening = f'listen_{message.member}'
            listening_handler = getattr(self, listening)
            asyncio.create_task(listening_handler(event))
        else:
            result = False

        return result
