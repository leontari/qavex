@dataclass(frozen=True, slots=True)
class DependencyId:
    """Unified identifier for the whole DI system."""

    namespace: Namespace
    contract: type[Any]


@dataclass(frozen=True, slots=True)
class DependencyDescriptor:
    id: DependencyId
    provider: Provider[Any]
    visibility: Visibility


@dataclass(slots=True)
class DependencyNode:
    id: DependencyId


@dataclass(frozen=True, slots=True)
class DependencyEdge:
    source: DependencyId
    target: DependencyId
