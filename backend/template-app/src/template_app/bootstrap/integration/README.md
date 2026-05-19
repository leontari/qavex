# Example usage

## Publisher module

```text
await context.event_bus.publish(
    UserCreatedEvent(
        user_id="123",
    )
)
```

## Subscriber module

```text
context.event_bus.subscribe(
    "user.created",
    self.handle_user_created,
)
```

## Example event

```text
from dataclasses import dataclass

from template_app.bootstrap.events.event import Event


@dataclass(slots=True)
class UserCreatedEvent(Event):

    user_id: str
```

## What it will provide
| Capability                   | 	Status |
|------------------------------|---------|
| Internal event orchestration | 	[ ]    |
| Plugin decoupling            | 	[ ]    |
| CQRS foundation              | 	[ ]    |
| Domain events                | 	[ ]    |
| Kafka bridge                 | 	[ ]    |
| Redis pub/sub bridge         | 	[ ]    |
| Async pipelines              | 	[ ]    |
| Sagas	                       | [ ]     |
| Workflow engine              | 	[ ]    |
