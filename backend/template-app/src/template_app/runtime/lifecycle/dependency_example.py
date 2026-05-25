LifecycleHook(
    name="database",
    handler=start_database,
)

LifecycleHook(
    name="cache",
    handler=start_cache,
    depends_on=frozenset({"database"}),
)

LifecycleHook(
    name="kafka",
    handler=start_kafka,
    depends_on=frozenset({"database"}),
)

LifecycleHook(
    name="http",
    handler=start_http,
    depends_on=frozenset({
        "database",
        "cache",
    }),
)
