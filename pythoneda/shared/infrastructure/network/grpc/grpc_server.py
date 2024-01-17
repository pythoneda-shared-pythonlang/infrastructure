# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/network/grpc/grpc_server.py

Base class for gRPC servers on PythonEDA applications.

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
import asyncio
import grpc
import logging
from pythoneda.shared import Event, PrimaryPort


class GrpcServer(PrimaryPort, abc.ABC):
    """
    Base class for gRPC servers on PythonEDA applications.

    Class name: GrpcServer

    Responsibilities:
        - Launch a gRPC server on a given port.
        - Provide extension hooks for subclasses.

    Collaborators:
        - pythoneda.application.PythonEDA: Sends notifications when the application is launched via CLI.
    """

    _default_insecure_port = "[::]:50051"

    def __init__(self, port=None):
        """
        Initializes a new GrpcServer instance.
        :param port: The gRPC port.
        :type port: int
        """
        super().__init__()
        self._app = None
        if port:
            self._insecure_port = port
        else:
            self._insecure_port = self.__class__._default_insecure_port

    @property
    def app(self):
        """
        Retrieves the PythonEDA application instance.
        :return: Such instance.
        :rtype: pythoneda.application.PythonEDA
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
        :param app: The PythonEDA application.
        :type app: pythoneda.application.PythonEDA
        """
        raise NotImplementedError("add_servicers() not implemented by {self.__class__}")

    async def accept(self, app):
        """
        A notification of the system being launched via CLI.
        :param app: The PythonEDA application.
        :type app: pythoneda.application.PythonEDA
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
        :param app: The PythonEDA application.
        :type app: pythoneda.application.PythonEDA
        """
        server = grpc.aio.server()
        self.add_servicers(server, app)
        server.add_insecure_port(self._insecure_port)
        logging.getLogger(__name__).info(
            f"gRPC server listening at {self.insecure_port}"
        )
        await server.start()
        await server.wait_for_termination()
