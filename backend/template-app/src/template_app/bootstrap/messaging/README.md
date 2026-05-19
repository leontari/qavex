## Runtime vs Distributed Messaging

### Runtime messaging

#### Used for:

- module-to-module communication
- plugin orchestration
- domain events
- CQRS
- internal workflows
- in-process pipelines

#### Works:

`inside single Python process`

#### Components:

```text
RuntimeEventBus
RuntimeCommandBus
RuntimeQueryBus
Distributed messaging
```

## Runtime vs Distributed Messaging

### Runtime messaging

#### Used for:

- service-to-service communication
- Kafka/NATS/Redis Streams integration
- remote command execution
- RPC queries
- integration events

#### Components:

```text
DistributedEventBridge
DistributedCommandGateway
RPCQueryGateway
```

# Example usage

## Publisher module

```text
from template_app.bootstrap.messaging.contracts.events import Event

class UserCreatedEvent(Event):
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id

await context.runtime.event_bus.publish(UserCreatedEvent(user_id="123"))
```

## Subscriber module

```text
from template_app.bootstrap.messaging.contracts.events import Event

class AuditHandler:
    async def __call__(self, event: Event) -> None:
        print(event)


context.runtime.messaging_registry.register_event_handler(
    UserCreatedEvent,
    AuditHandler(),
)
```

## Example command

```text
from dataclasses import dataclass
from template_app.bootstrap.messaging.contracts.commands import Command

@dataclass(slots=True)
class CreateUserCommand(Command):
    email: str
```

## Command execution
```text
await context.runtime.command_bus.execute(
    CreateUserCommand(
        email="admin@example.com",
    )
)
```

## Command handler registration

```text
async def create_user_handler(command: CreateUserCommand) -> None:
    print(command.email)


context.runtime.messaging_registry.register_command_handler(
    CreateUserCommand,
    create_user_handler,
)
```

## Example query

```text
from dataclasses import dataclass

from template_app.bootstrap.messaging.contracts.queries import Query


@dataclass(slots=True)
class GetUserQuery(Query):
    user_id: str
```

## Query execution
```text
result = await context.runtime.query_bus.ask(
    GetUserQuery(
        user_id="123",
    )
)
```

## Query handler registration
```text
async def get_user_handler(query: GetUserQuery) -> dict[str, str]:
    return {
        "id": query.user_id,
        "name": "admin",
    }


context.runtime.messaging_registry.register_query_handler(
    GetUserQuery,
    get_user_handler,
)
```
