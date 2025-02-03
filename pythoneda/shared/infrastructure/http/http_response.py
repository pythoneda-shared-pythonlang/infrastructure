# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/http/http_response.py

This file defines the HttpResponse class.

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
from org.acmsl.licdata.events.clients import (
    ListClientsRequested,
    NoMatchingClientsFound,
)
from pythoneda.shared import Event
from typing import Dict, Type


class HttpResponse(Event, abc.ABC):
    """
    Base class for HTTP responses.

    Class name: HttpResponse

    Responsibilities:
        - Defines the HTTP responses.

    Collaborators:
        - None
    """

    def __init__(self, responseEvent: Event, sourceEvent: Event):
        """
        Creates a new HttpResponse.
        :param event: The domain event, generated after the source event.
        :type event: pythoneda.shared.Event
        :param sourceEvent: The source event.
        :type sourceEvent: pythoneda.shared.Event
        """
        super().__init__()
        self._response_event = responseEvent
        self._source_event = sourceEvent

    @property
    def response_event(self) -> Event:
        """
        Retrieves the response event.
        :return: The response event.
        :type: pythoneda.shared.Event
        """
        return self._response_event

    @property
    def source_event(self) -> ListClientsRequested:
        """
        Retrieves the source event.
        :return: The source event.
        :type: org.acmsl.licdata.events.clients.ListClientsRequested
        """
        return self._source_event

    @property
    def status_code(self) -> int:
        """
        Retrieves the status code.
        :return: The status code.
        :type: int
        """
        return 200

    @property
    def body(self) -> Dict:
        """
        Retrieves the body.
        :return: The body.
        :type: Dict
        """
        return {}

    @property
    def headers(self) -> Dict:
        """
        Retrieves the headers.
        :return: The headers.
        :type: Dict
        """
        return {}

    @property
    def mime_type(self) -> str:
        """
        Retrieves the MIME type.
        :return: The MIME type.
        :type: str
        """
        return "application/json"

    @property
    def charset(self) -> str:
        """
        Retrieves the charset.
        :return: The charset.
        :type: str
        """
        return "utf-8"

    @classmethod
    @abc.abstractmethod
    def event_class(cls) -> Type[Event]:
        """
        Retrieves the class of the response event.
        :return: The class.
        :type: Type[pythoneda.shared.Event]
        """
        pass


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
