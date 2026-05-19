"""
Internal runtime inter-module integration.

Responsible for:
    cross modules integration

Inter module communicating bus.

module A ↔ EventBus ↔ module B

Examples:
    Module A
    └── emits UserRegisteredEvent

    NotificationModule
    └── handles UserRegisteredEvent

    Module B
    └── handles UserRegisteredEvent

Event bus characteristics:
Feature	      Value
delivery	broadcast
handlers	many
response	none
coupling	low
execution	async/event-driven
purpose	    integration

"""

from __future__ import annotations
