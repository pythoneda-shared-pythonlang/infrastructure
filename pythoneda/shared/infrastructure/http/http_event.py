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
import base64
from .http_method import HttpMethod
from pythoneda.shared import attribute, BaseObject, Event
from typing import Dict, Optional, Tuple, Type


class HttpEvent(BaseObject, abc.ABC):
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
        httpMethod: HttpMethod,
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
        (params, error) = self._process()
        if error:
            raise ValueError(f"Invalid input")
        else:
            self._processed_params = params

    @property
    @attribute
    def http_method(self) -> HttpMethod:
        """
        Retrieves the HTTP method.
        :return: The HTTP method.
        :rtype: pythoneda.shared.infrastructure.http.HttpMethod
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

    @abc.abstractmethod
    def to_event(self) -> Event:
        """
        Retrieves the event.
        :return: The event.
        :rtype: Event
        """
        pass

    @classmethod
    @abc.abstractmethod
    def event_class(cls) -> Type[Event]:
        """
        Retrieves the class of the event.
        :return: The class.
        :type: Type[pythoneda.shared.Event]
        """
        pass

    def _process(self) -> Tuple[Dict, bool]:
        """
        Processes the input data and converts it to a dictionary.
        :return: A tuple with the body and the error, if any.
        :rtype: Tuple[Dict, bool]
        """
        result = {}
        error = True
        errors = []
        if self.body is None:
            errors.append("Missing 'body'")
        else:
            if type(self.body) is dict:
                result["body"] = self.body
                error = False
            elif type(self.body) is str:
                try:
                    result["body"] = json.loads(self.body)
                    error = False
                except Exception as encoding_error:
                    try:
                        result["body"] = json.loads(
                            base64.decodebytes(str.encode(self.body))
                        )
                        error = False
                    except Exception as giving_up:
                        errors.append(
                            f"Body not in JSON format or not base64-encoded: {giving_up}"
                        ),
                        errors.append(f"Body not in JSON format: {encoding_error}")
            else:
                errors.append(f"Unknown body type: {type(self.body)}")

        result["http_method"] = self.http_method
        result["query_string_parameters"] = self.query_string_parameters
        result["headers"] = self.headers
        result["path_parameters"] = self.path_parameters
        if len(errors) > 0:
            result["errors"] = errors
        return (result, error)

    def retrieve_param(self, paramName: str, defaultValue) -> str:
        """
        Retrieves the value of given parameter.
        :param paramName: The name of the parameter.
        :type paramName: str
        :param defaultValue: The default value if the parameter is missing.
        :type defaultValue: str
        :return: The value of the parameter.
        :rtype: str
        """
        result = None

        body = self._processed_params.get("body", None)
        if body is not None:
            result = body.get(paramName, None)

        if result is None:
            path_params = self._processed_params.get("path_parameters", None)
            if path_params is not None:
                result = path_params.get(paramName, None)

        if result is None:
            query_string_params = self._processed_params.get(
                "query_string_parameters", None
            )
            if query_string_params is not None:
                result = query_string_params.get(paramName, None)

        return result

    def retrieve_id(self) -> str:
        """
        Retrieves the value of the 'id' parameter.
        :return: The id.
        :rtype: str
        """
        return self.retrieve_param("id", None)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
