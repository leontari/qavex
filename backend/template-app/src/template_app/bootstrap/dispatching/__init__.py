"""
Application execution dispatching.

Responsible for:
    request execution

Strict execution layer:
request -> handler -> response

CommandBus:
    CreateModuleACommand
        -> CreateModuleHandler
QueryBus:
    GetModuleAQuery
        -> GetModuleAHandler
        -> returns ModuleDTO

Messaging characteristics
Feature	       Value
delivery	point-to-point
handlers	exactly one
response	required
coupling	stronger
execution	request/response
purpose	    application execution

"""

from __future__ import annotations
