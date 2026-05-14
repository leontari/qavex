from __future__ import annotations

import asyncio

from template_app.health.plugins.base import HealthCheckPlugin
from template_app.health.executor.context import ExecutionContext
from template_app.health.executor.layer_builder import LayerBuilder


class DependencyGraphExecutor:
    """
    Executes health plugins respecting dependency graph layers.

    This is NOT just execution — it's orchestration.
    """

    def __init__(self, executor):
        self.executor = executor
        self.layer_builder = LayerBuilder()

    async def execute(
        self,
        plugins: dict[str, HealthCheckPlugin],
    ):
        """
        Dependency-aware execution.
        """

        # 1. Build dependency map
        graph = {name: plugin.dependencies for name, plugin in plugins.items()}

        layers = self.layer_builder.build_layers(graph)

        ctx = ExecutionContext()

        results = []

        # 2. Execute layer by layer
        for layer in layers:
            tasks = []

            for name in layer:
                plugin = plugins[name]

                # 2.1 Skip logic (critical)
                if any(dep in ctx.failed for dep in plugin.dependencies):
                    ctx.skipped.add(name)
                    continue

                tasks.append(self._run(plugin, ctx))

            layer_results = await asyncio.gather(*tasks)

            results.extend(layer_results)

        return results

    async def _run(self, plugin, ctx: ExecutionContext):
        result = await self.executor.execute(plugin)

        ctx.results[plugin.name] = result

        if result.status == "unhealthy":
            ctx.failed.add(plugin.name)

        return result
