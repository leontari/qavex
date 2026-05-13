"""
Lifecycle orchestration engine.

LifecycleManager = composition root

Startup order:
1. logging
2. config load
3. db engine
4. redis/kafka
5. health registry
6. warmup caches
7. background tasks
8. mark READY

"""
