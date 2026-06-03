import inspect

from template_app.launcher.facade import run_http, run_grpc, run_kafka, run_cli
from template_app.runtime.transports.cli.entrypoint import (
    run_cli_runtime,
)
from template_app.runtime.transports.grpc.entrypoint import (
    run_grpc_runtime,
)
from template_app.runtime.transports.http.entrypoint import (
    run_http_runtime,
)
from template_app.runtime.transports.kafka.entrypoint import (
    run_kafka_runtime,
)


def test_runtime_entrypoints_have_same_signature():
    """Protect from api change."""
    expected = ["kernel", "config"]

    for fn in (
        run_http_runtime,
        run_grpc_runtime,
        run_kafka_runtime,
        run_cli_runtime,
    ):
        params = list(inspect.signature(fn).parameters)

        assert params == expected


def test_runtime_facades_exist() -> None:
    assert callable(run_http)
    assert callable(run_grpc)
    assert callable(run_kafka)
    assert callable(run_cli)
