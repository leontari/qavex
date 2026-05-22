from fastapi import APIRouter, FastAPI

from template_app.bootstrap.kernel import RuntimeKernel


class FastApiTransport:
    def __init__(self, app: FastAPI, kernel: RuntimeKernel):
        self.app = app
        self.kernel = kernel

    async def startup(self) -> None: ...

    async def shutdown(self) -> None: ...

    def register_router(self, router: APIRouter) -> None:
        self.app.include_router(router)
