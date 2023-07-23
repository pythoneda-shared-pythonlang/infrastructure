"""
pythonedainfrastructure/pythonedanetwork/pythonedagrpc/pythoneda_grpc_server.py

Base class for gRPC servers on PythonEDA applications.

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
from pythoneda.event import Event
from pythoneda.primary_port import PrimaryPort

import abc
from concurrent import futures
import grpc

import asyncio
import time
import json
import logging
from typing import Dict

class PythonedaGrpcServer(PrimaryPort, abc.ABC):
    """
    Base class for gRPC servers on PythonEDA applications.

    Class name: PythonedaGrpcServer

    Responsibilities:
        - Launch a gRPC server on a given port.
        - Provide extension hooks for subclasses.

    Collaborators:
        - pythonedaapplication.PythonEDAApplication: Sends notifications when the application is launched via CLI.
    """

    _default_insecure_port = '[::]:50051'

    def __init__(self, port=None):
        """
        Initializes the instance.
        :param port: The gRPC port.
        :type port: int
        """
        super().__init__()
        if port:
            self._insecure_port = port
        else:
            self._insecure_port = self.__class__._default_insecure_port

    @property
    def app(self):
        """
        Retrieves the PythonEDAApplication instance.
        :return: Such instance.
        :rtype: PythonEDAApplication
        """
        return self._app

    @property
    def insecure_port(self) -> str:
        """
        Retrieves the insecure port of the gRPC server.
        :return: Such port.
        :rtype: str
        """
        return self._insecure_port

    def priority(self) -> int:
        """
        Retrieves the priority of this CLI handler.
        :return: Such value.
        :rtype: int
        """
        return 999

    @abc.abstractmethod
    def add_servicers(self, server, app):
        """
        Adds servicers to given server.
        :param server: The gRPC server.
        :type server: grpc.aio.Server
        :param app: The PythonEDAApplication instance.
        :type app: pythonedaapplication.PythonEDAApplication
        """
        raise NotImplementedError("add_servicers() not implemented by {self.__class__}")

    async def accept(self, app):
        """
        A notification of the system being launched via CLI.
        :param app: The PythonEDAApplication instance.
        :type app: pythonedaapplication.PythonEDAApplication
        """
        self._app = app
        serve_task = asyncio.create_task(self.serve(app))
        asyncio.ensure_future(serve_task)
        try:
            await serve_task
        except KeyboardInterrupt:
            serve_task.cancel()
            try:
                await serve_task
            except asyncio.CancelledError:
                pass

    async def serve(self, app):
        """
        Starts the gRPC server.
        :param app: The PythonEDAApplication instance.
        :type app: pythonedaapplication.PythonEDAApplication
        """
        server = grpc.aio.server()
        self.add_servicers(server, app)
        server.add_insecure_port(self._insecure_port)
        logging.getLogger(__name__).info(f'gRPC server listening at {self.insecure_port}')
        await server.start()
        await server.wait_for_termination()
