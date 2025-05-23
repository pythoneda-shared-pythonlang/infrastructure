# vim: set fileencoding=utf-8
"""
pythoneda/shared/infrastructure/azure/functions/__init__.py

This file ensures pythoneda.shared.infrastructure.azure.functions is a namespace.

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
import os, importlib
from pythoneda.shared import Invariant, Invariants, PythonedaApplication
from typing import Type

__path__ = __import__("pkgutil").extend_path(__path__, __name__)


pythoneda_app_default = None


def get_class_from_env() -> Type[PythonedaApplication]:
    """
    Retrieves the application to set as invariant.
    :return: Such class.
    :rtype: Type[pythoneda.shared.PythonedaApplication]
    """
    class_path = os.environ["PYTHONEDA_APP_FOR_AZURE_FUNCTIONS"]
    module_name, class_name = class_path.rsplit(".", 1)
    mod = importlib.import_module(module_name)
    cls = getattr(mod, class_name)
    return cls


def get_pythoneda_app() -> PythonedaApplication:
    """
    Retrieves the PythonEDA application.
    :return: The PythonEDA application.
    :rtype: pythoneda.shared.PythonedaApplication
    """
    global pythoneda_app_default
    result = Invariants.instance().apply("pythoneda.shared.PythonedaApplication", None)
    if result is None:
        result = pythoneda_app_default
    elif pythoneda_app_default is None:
        pythoneda_app_default = result.value
    else:
        result = pythoneda_app_default

    return result


async def run_main():
    """
    Runs the main method of the PythonEDA application.
    """
    if get_pythoneda_app() is None:
        app_class = get_class_from_env()
        result = await app_class.main()
    else:
        result = None

    return result


def on_main_done(fut: asyncio.Future):
    """
    Callback for when the main method is done.
    :param fut: The future.
    :type fut: asyncio.Future
    """
    global pythoneda_app_default
    app = fut.result()
    if pythoneda_app_default is None:
        pythoneda_app_default = app


if os.environ.get("PYTHONEDA_ENABLE_AZURE_FUNCTIONS", None) is not None:
    if get_pythoneda_app() is None:
        loop = asyncio.get_event_loop()
        loop.create_task(run_main())


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
