# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/http/http_event.py

This file defines the HttpEvent class.

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
from pythoneda.shared import Event
from typing import Dict


class HttpEvent(Event, abc.ABC):
    """
    HTTP interface for events.

    Class name: HttpEvents

    Responsibilities:
        - Define the HTTP interface for events.

    Collaborators:
        - None
    """

    def __init__(
        self,
        httpMethod: str,
        queryStringParameters: Dict,
        headers: Dict,
        pathParameters: Dict,
        body: Dict,
    ):
        """
        Creates a new HttpEvent.
        :param httpMethod: The HTTP method.
        :type httpMethod: str
        :param queryStringParameters: The query string parameters.
        :type queryStringParameters: Dict
        :param headers: The headers.
        :type headers: Dict
        :param pathParameters: The path parameters.
        :type pathParameters: Dict
        :param body: The body.
        :type body: Dict
        """
        super().__init__()
        self._http_method = httpMethod
        self._query_string_parameters = queryStringParameters
        self._headers = headers
        self._path_parameters = pathParameters
        self._body = body

    @property
    @attribute
    def http_method(self) -> str:
        """
        Retrieves the HTTP method.
        :return: The HTTP method.
        :rtype: str
        """
        return self._http_method

    @property
    @attribute
    def query_string_parameters(self) -> Dict:
        """
        Retrieves the query string parameters.
        :return: The query string parameters.
        :rtype: Dict
        """
        return self._query_string_parameters

    @property
    @attribute
    def headers(self) -> Dict:
        """
        Retrieves the headers.
        :return: The headers.
        :rtype: Dict
        """
        return self._headers

    @property
    @attribute
    def path_parameters(self) -> Dict:
        """
        Retrieves the path parameters.
        :return: The path parameters.
        :rtype: Dict
        """
        return self._path_parameters

    @property
    @attribute
    def body(self) -> Dict:
        """
        Retrieves the body.
        :return: The body.
        :rtype: Dict
        """
        return self._body


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
