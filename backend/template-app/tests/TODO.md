# тест на корректный импорт приложения

написать конкретный Dockerfile + CI‑скрипт, который:
- собирает wheel,
- устанавливает его,
- прогоняет pytest,
- (опционально) прогоняет Alembic миграции.

возможно alembic миграции нужно вынести в отдельный сервис!!!

## Самый полезный уровень тестов для рефакторинга

1. Contract tests:
- imports
- routes
- middleware
- DI
- settings
- startup order

2. Wiring tests:
- router registration
- service injection
- repository injection
- lifespan hooks

3. Pure unit tests:
- services
- validators
- utils
- repositories
