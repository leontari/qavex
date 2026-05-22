from fastapi import FastAPI


def build_test_transport() -> FastAPI:
    return FastAPI(
        title="test-app",
    )
