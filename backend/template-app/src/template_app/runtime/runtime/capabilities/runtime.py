"""Runtime capability builder."""

from __future__ import annotations

from template_app.runtime.runtime.capabilities.models import (
    RuntimeCapabilities,
)
from template_app.runtime.transports.http.transport import (
    FastAPITransport,
)
from template_app.runtime.transports.kafka.transport import (
    KafkaTransport,
)
from template_app.runtime.transports.grpc.transport import (
    GRPCTransport,
)
from template_app.runtime.transports.cli.transport import (
    CLITransport,
)


def build_runtime_capabilities(runtime) -> RuntimeCapabilities:
    """
    Build runtime capability descriptor.

    Args:
        runtime:
            Runtime graph.

    Returns:
        Runtime capability descriptor.

    """
    transports = runtime.transports.manager.transports

    return RuntimeCapabilities(
        http=any(isinstance(t, FastAPITransport) for t in transports),
        kafka=any(isinstance(t, KafkaTransport) for t in transports),
        grpc=any(isinstance(t, GRPCTransport) for t in transports),
        cli=any(isinstance(t, CLITransport) for t in transports),
        lifecycle=True,
        messaging=True,
        infrastructure=True,
        modules=True,
    )
