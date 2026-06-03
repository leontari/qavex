from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from template_app.runtime.modules.apis.runtime import ModuleRuntimeAPI

if TYPE_CHECKING:
    from fastapi import APIRouter, FastAPI


@dataclass(slots=True)
class FastAPIModuleRuntimeAPI(ModuleRuntimeAPI):
    app: FastAPI

    def register_router(self, router: APIRouter) -> None:
        self.app.include_router(router)
