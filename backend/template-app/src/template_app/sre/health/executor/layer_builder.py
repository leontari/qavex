from __future__ import annotations

from collections import defaultdict, deque


class LayerBuilder:
    """
    Converts dependency graph into execution layers.
    """

    def build_layers(
        self,
        nodes: dict[str, set[str]],
    ) -> list[list[str]]:
        """
        Returns:
            [
              ["db", "redis"],        # layer 0
              ["user_service"],       # layer 1
              ["api_gateway"]         # layer 2
            ]
        """

        indegree = defaultdict(int)
        graph = defaultdict(list)

        for node, deps in nodes.items():
            for dep in deps:
                graph[dep].append(node)
                indegree[node] += 1

        queue = deque([n for n in nodes if indegree[n] == 0])

        layers: list[list[str]] = []

        while queue:
            size = len(queue)
            layer = []

            for _ in range(size):
                node = queue.popleft()
                layer.append(node)

                for child in graph[node]:
                    indegree[child] -= 1
                    if indegree[child] == 0:
                        queue.append(child)

            layers.append(layer)

        return layers
